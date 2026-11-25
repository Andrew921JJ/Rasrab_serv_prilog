from flask import jsonify, request, g
from pydantic import ValidationError
from app.domain.errors import ErrNotFound, ErrAlreadyExists, ErrConflict, ErrInvalidInput
import logging
import uuid

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    # B7: Генерация X-Request-ID (middleware)
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

    @app.after_request
    def add_request_id_header(response):
        response.headers['X-Request-ID'] = g.get('request_id', 'unknown')
        return response

    # B6: Единый формат ошибки
    def make_error_response(code: str, message: str, status_code: int, details=None):
        response = {
            "error": {
                "code": code,
                "message": message,
                "request_id": g.get('request_id', 'unknown')
            }
        }
        if details:
            response["error"]["details"] = details
        return jsonify(response), status_code

    # B3, B4: Ошибки валидации Pydantic (400 Bad Request)
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        details = []
        for error in e.errors():
            details.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"]
            })
        return make_error_response("VALIDATION_ERROR", "Ошибка валидации входных данных", 400, details)

    # Обработка доменных ошибок
    @app.errorhandler(ErrNotFound)
    def handle_not_found(e):
        return make_error_response("NOT_FOUND", str(e), 404)

    @app.errorhandler(ErrAlreadyExists)
    def handle_already_exists(e):
        return make_error_response("ALREADY_EXISTS", str(e), 409)

    @app.errorhandler(ErrConflict)
    def handle_conflict(e):
        return make_error_response("CONFLICT", str(e), 409)

    @app.errorhandler(ErrInvalidInput)
    def handle_invalid_input(e):
        return make_error_response("INVALID_INPUT", str(e), 422)

    # B7: Обработка 500 (Скрываем детали, пишем в лог)
    @app.errorhandler(Exception)
    def handle_internal_error(e):
        req_id = g.get('request_id', 'unknown')
        logger.exception(f"Internal Server Error [Request ID: {req_id}]: {str(e)}")
        # Клиент видит только общее сообщение
        return make_error_response("INTERNAL_SERVER_ERROR", "Внутренняя ошибка сервера", 500)