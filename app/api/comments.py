from flask import Blueprint, request, jsonify
from app.services.post_service import PostService
from app.services.comment_service import CommentService
from app.infrastructure.repositories_pg import PgPostRepository

posts_bp = Blueprint('posts', __name__)
# Инициализируем репозиторий и сервис (в реальном проекте это делается через DI-контейнер)
# Для простоты можно передавать репозиторий через app.config
def get_post_service():
    return PostService(request.app.config['POST_REPO'])

@posts_bp.route('/', methods=['POST'])
def create_post():
    data = request.get_json()
    service = get_post_service()
    # В реальности author_id берется из токена аутентификации
    dto = service.create_post(author_id=data['author_id'], title=data['title'], content=data['content'])
    
    # Требование T6: Возврат заголовка Location при создании
    response = jsonify(dto.__dict__)
    response.status_code = 201
    response.headers['Location'] = f"/api/posts/{dto.id}"
    return response

@posts_bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    service = get_post_service()
    dto = service.get_post(post_id)
    return jsonify(dto.__dict__)

@posts_bp.route('/', methods=['GET'])
def list_posts():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    service = get_post_service()
    dtos = service.list_posts(limit, offset)
    return jsonify([d.__dict__ for d in dtos])

@posts_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    service = get_post_service()
    dto = service.update_post(post_id, data['title'], data['content'])
    return jsonify(dto.__dict__)

@posts_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    service = get_post_service()
    service.delete_post(post_id)
    return '', 204