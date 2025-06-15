# api_bp.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, logout_user
from db_instance import db
from models import User, News
from utils.validators import validate_user_data

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')


# --- API для новостей ---
@api_bp.route('/news', methods=['GET'])
def get_news_api():
    news_list = News.query.all()
    return jsonify([news.to_dict(include_author=True) for news in news_list])


@api_bp.route('/news/<int:news_id>', methods=['GET'])
def get_single_news_api(news_id):
    news = db.session.get(News, news_id)
    if news is None:
        return jsonify({'message': 'Новость не найдена'}), 404
    return jsonify(news.to_dict(include_author=True))


@api_bp.route('/news', methods=['POST'])
@login_required
def add_news_api():
    data = request.json
    if not data:
        return jsonify({'message': 'Отсутствуют данные в формате JSON'}), 400

    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': 'Заголовок и содержание обязательны'}), 400

    if len(title) > 100 or len(title) < 1:
        return jsonify({'message': 'Заголовок должен быть от 1 до 100 символов'}), 400

    news = News(title=title, content=content, user_id=current_user.id)
    db.session.add(news)
    db.session.commit()
    return jsonify(news.to_dict()), 201


@api_bp.route('/news/<int:news_id>', methods=['PUT'])
@login_required
def update_news_api(news_id):
    news = db.session.get(News, news_id)
    if news is None:
        return jsonify({'message': 'Новость не найдена'}), 404

    if news.user_id != current_user.id:
        return jsonify({'message': 'Вы можете редактировать только свои новости'}), 403

    data = request.json
    if not data:
        return jsonify({'message': 'Отсутствуют данные в формате JSON'}), 400

    title = data.get('title')
    content = data.get('content')

    if title:
        if len(title) > 100 or len(title) < 1:
            return jsonify({'message': 'Заголовок должен быть от 1 до 100 символов'}), 400
        news.title = title
    if content:
        news.content = content

    db.session.commit()
    return jsonify(news.to_dict())


@api_bp.route('/news/<int:news_id>', methods=['DELETE'])
@login_required
def delete_news_api(news_id):
    news = db.session.get(News, news_id)
    if news is None:
        return jsonify({'message': 'Новость не найдена'}), 404

    if news.user_id != current_user.id:
        return jsonify({'message': 'Вы можете удалить только свои новости'}), 403

    db.session.delete(news)
    db.session.commit()
    return jsonify({'message': 'Новость успешно удалена'}), 204  # 204 No Content for successful deletion


# --- API для пользователей ---


@api_bp.route('/users', methods=['GET'])
def get_users_api():
    users_list = User.query.all()
    return jsonify([user.to_dict() for user in users_list])


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_single_user_api(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({'message': 'Пользователь не найден'}), 404
    return jsonify(user.to_dict())


@api_bp.route('/users', methods=['POST'])
def register_user_api():
    data = request.json
    if not data:
        return jsonify({'message': 'Отсутствуют данные в формате JSON'}), 400

    errors = validate_user_data(data)
    if errors:
        return jsonify({'message': 'Ошибка валидации', 'errors': errors}), 400

    email = data.get('email')
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Этот email уже зарегистрирован'}), 400

    user = User(first_name=data['first_name'],
                last_name=data['last_name'],
                email=email)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user_api(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({'message': 'Пользователь не найден'}), 404

    # Пользователь может редактировать только свой профиль, если он не администратор
    if user.id != current_user.id:
        return jsonify({'message': 'Вы можете редактировать только свой профиль'}), 403

    data = request.json
    if not data:
        return jsonify({'message': 'Отсутствуют данные в формате JSON'}), 400

    errors = validate_user_data(data, is_update=True)
    if errors:
        return jsonify({'message': 'Ошибка валидации', 'errors': errors}), 400

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        # Проверяем, не занят ли новый email другим пользователем
        if User.query.filter(User.email == data['email'], User.id != user.id).first():
            return jsonify({'message': 'Этот email уже зарегистрирован другим пользователем'}), 400
        user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.to_dict())


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user_api(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({'message': 'Пользователь не найден'}), 404

    # Пользователь может удалить только свой профиль, если он не администратор
    if user.id != current_user.id:
        return jsonify({'message': 'Вы можете удалить только свой профиль'}), 403

    # При удалении пользователя, связанные новости будут удалены благодаря cascade='all, delete-orphan'
    db.session.delete(user)
    db.session.commit()
    logout_user()  # Выход из системы после удаления своего аккаунта
    return jsonify({'message': 'Пользователь успешно удален'}), 204