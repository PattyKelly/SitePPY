from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple in-memory user storage (for demonstration purposes)
users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'name': 'Administrador'
    },
    'user': {
        'password': generate_password_hash('user123'),
        'name': 'Usuário'
    }
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.name = users[username]['name']

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

def is_safe_url(target):
    """
    Check if a URL is safe to redirect to.
    
    This function validates that the redirect URL:
    - Uses http or https scheme
    - Points to the same domain as the current request
    
    This prevents open redirect vulnerabilities where an attacker could
    redirect users to malicious external sites.
    
    Args:
        target: The URL to validate
        
    Returns:
        bool: True if URL is safe, False otherwise
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            
            # Safely handle redirect to prevent open redirect vulnerability
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Use debug mode only in development. Set FLASK_DEBUG=0 or remove for production
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
