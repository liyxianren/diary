from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 基础配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///diary.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 初始化扩展
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# 用户模型
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # 密码重置字段
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

# 用户注册API
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # 验证输入
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400

        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']

        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409

        # 创建新用户
        password_hash = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db.session.add(new_user)
        db.session.commit()

        # 创建访问令牌
        access_token = create_access_token(identity=str(new_user.id))

        return jsonify({
            'message': '用户注册成功',
            'access_token': access_token,
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'注册失败: {str(e)}'}), 500

# 用户登录API
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data.get('username') or not data.get('password'):
            return jsonify({'error': '请输入用户名和密码'}), 400

        username = data['username'].strip()
        password = data['password']

        # 查找用户（支持用户名或邮箱）
        user = User.query.filter(
            (User.username == username) | (User.email == username.lower())
        ).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': '用户名/邮箱或密码错误'}), 401

        if not user.is_active:
            return jsonify({'error': '账号已被停用'}), 403

        # 创建访问令牌
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

# 获取用户信息API
@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

# 登录页面路由
@app.route('/login')
def login_page():
    return render_template('login.html')

# 注册页面路由
@app.route('/register')
def register_page():
    return render_template('register.html')

# 重置密码页面路由
@app.route('/reset-password/<token>')
def reset_password_page(token):
    return render_template('reset_password.html', token=token)

# 忘记密码API - 发送重置链接
@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({'error': '请输入邮箱地址'}), 400

        # 检查邮箱是否存在
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': '该邮箱未注册'}), 404

        # 生成重置令牌（有效期1小时）
        reset_token = generate_password_hash(f"{user.id}{datetime.utcnow().isoformat()}")[:50]
        user.reset_token = reset_token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()

        # 这里应该发送邮件，暂时返回成功消息
        return jsonify({
            'message': '重置链接已发送到您的邮箱',
            'reset_token': reset_token  # 开发环境返回，生产环境应删除
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'发送失败: {str(e)}'}), 500

# 重置密码API
@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        reset_token = data.get('reset_token')
        new_password = data.get('new_password')

        if not reset_token or not new_password:
            return jsonify({'error': '缺少必要参数'}), 400

        if len(new_password) < 6:
            return jsonify({'error': '密码长度至少为6个字符'}), 400

        # 查找用户
        user = User.query.filter_by(reset_token=reset_token).first()
        if not user:
            return jsonify({'error': '无效的重置链接'}), 404

        # 检查链接是否过期
        if not user.reset_token_expires or datetime.utcnow() > user.reset_token_expires:
            return jsonify({'error': '重置链接已过期'}), 400

        # 更新密码
        user.password_hash = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()

        return jsonify({'message': '密码重置成功'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'重置失败: {str(e)}'}), 500

# 健康检查API
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

def upgrade_database():
    """升级数据库结构"""
    with app.app_context():
        try:
            # 检查是否需要添加重置令牌字段
            engine = db.engine
            inspector = db.inspect(engine)
            columns = inspector.get_columns('users')
            column_names = [col['name'] for col in columns]

            if 'reset_token' not in column_names:
                print("正在添加重置令牌字段...")
                with engine.connect() as conn:
                    conn.execute(db.text("""
                        ALTER TABLE users
                        ADD COLUMN reset_token VARCHAR(255),
                        ADD COLUMN reset_token_expires DATETIME
                    """))
                    conn.commit()
                print("重置令牌字段添加成功")

        except Exception as e:
            print(f"数据库升级失败: {e}")

if __name__ == '__main__':
    with app.app_context():
        # 先升级数据库结构
        upgrade_database()
        # 然后创建表（如果不存在）
        db.create_all()

    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)