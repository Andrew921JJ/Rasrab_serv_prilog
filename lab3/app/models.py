import uuid
from datetime import datetime
from app.db import db

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    # В MySQL CHAR(36) используется для UUID
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    # ENUM в MySQL
    role = db.Column(db.Enum('admin', 'moderator', 'user', name='user_roles'), default='user')
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    # LONGTEXT из ERD
    content = db.Column(db.Text(length=4294967295), nullable=False) 
    status = db.Column(db.Enum('draft', 'published', 'archived', name='post_status'), default='draft')
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.String(36), db.ForeignKey('comments.id')) 
    content = db.Column(db.Text, nullable=False)
    is_moderated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

# Связующая таблица Post-Tag
post_tags = db.Table('post_tags',
    db.Column('post_id', db.String(36), db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)