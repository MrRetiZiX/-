from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, User, News
import telegram

# Глобальный словарь для хранения кодов верификации
verification_codes = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eco_valley.db'

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Инициализация базы данных
db.init_app(app)

# Создаём все таблицы
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/news')
def news():
    # Парсим новости с экологических сайтов
    news_items = News.query.order_by(News.published_at.desc()).limit(10).all()
    return render_template('news.html', news=news_items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        code = request.form.get('verification_code')
        
        # Проверяем код верификации
        for telegram_id, stored_code in verification_codes.items():
            if stored_code == code:
                # Код верный, создаём пользователя
                user = User(
                    username=request.form['username'],
                    email=request.form['email'],
                    password=request.form['password'],
                    telegram_id=telegram_id,
                    verification_code=code
                )
                db.session.add(user)
                db.session.commit()
                
                # Удаляем использованный код
                del verification_codes[telegram_id]
                
                login_user(user)
                return redirect(url_for('home'))
                
        flash('Неверный код верификации')
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/verify-code', methods=['POST'])
def verify_code():
    code = request.json.get('code')
    is_valid = code in verification_codes.values()
    return jsonify({'valid': is_valid})
