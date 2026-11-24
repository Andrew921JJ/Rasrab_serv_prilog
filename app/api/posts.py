from flask import Blueprint, request, jsonify, current_app
from app.services.post_service import PostService
from app.api.dto import PostDTO

posts_bp = Blueprint('posts', __name__)

# Вспомогательная функция для получения сервиса
def get_post_service():
    # Берем репозиторий из конфига, который мы положили в create_app
    post_repo = current_app.config['POST_REPO']
    return PostService(post_repo)

@posts_bp.route('/', methods=['POST'])
def create_post():
    data = request.get_json()
    service = get_post_service()
    
    # В реальности author_id берется из токена, но для лабы передадим в JSON
    dto = service.create_post(
        author_id=data['author_id'], 
        title=data['title'], 
        content=data['content']
    )
    
    # T6: Возвращаем заголовок Location при создании
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