# app.py
from flask import Flask, jsonify, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from db_instance import db
from models import User, News
from forms import LoginForm, RegistrationForm, NewsForm
from api_bp import api_bp

# Инициализация Flask приложения
app = Flask(__name__)

# Загрузка конфигурации
app.config.from_object('config.Config')

# Инициализация SQLAlchemy
db.init_app(app)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """
    Для загрузки пользователя по его ID из сессии.
    """
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

# Регистрация Blueprint API
app.register_blueprint(api_bp)

# --- Фронтенд маршруты ---

@app.route('/')
@app.route('/index')
def index():
    # Получаем все новости для отображения на главной странице
    news_list = News.query.all()
    return render_template('index.html', title='Главная', news=news_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный email или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Вы успешно вошли в систему!')
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы успешно зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(news)
        db.session.commit()
        flash('Ваша новость успешно добавлена!')
        return redirect(url_for('index'))
    return render_template('add_news.html', title='Добавить новость', form=form)

@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news = db.session.get(News, news_id)
    if news is None:
        flash('Новость не найдена.')
        return redirect(url_for('index'))

    if news.user_id != current_user.id:
        flash('Вы можете редактировать только свои новости.')
        return redirect(url_for('index'))

    form = NewsForm()
    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        db.session.commit()
        flash('Ваша новость успешно обновлена!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = news.title
        form.content.data = news.content
    return render_template('edit_news.html', title='Редактировать новость', form=form)

@app.route('/delete_news/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    news = db.session.get(News, news_id)
    if news is None:
        flash('Новость не найдена.')
        return redirect(url_for('index'))

    if news.user_id != current_user.id:
        flash('Вы можете удалить только свои новости.')
        return redirect(url_for('index'))

    db.session.delete(news)
    db.session.commit()
    flash('Новость успешно удалена!')
    return redirect(url_for('index'))


# --- Обработчики ошибок Flask ---
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request', 'details': str(error)}), 400

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({'error': 'Forbidden'}), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Обработчик, когда пользователь не авторизован
#@login_manager.unauthorized_handler
#def unauthorized():
#    return jsonify({"message": "Unauthorized: Login required"}), 401

@login_manager.unauthorized_handler
def unauthorized():
    flash('Для доступа к этой странице необходимо войти в систему.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
