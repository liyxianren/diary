# 路由模块初始化
from flask import Blueprint

# 创建蓝图
auth_bp = Blueprint('auth', __name__)
diary_bp = Blueprint('diary', __name__)

# 导入路由处理器
from . import auth, diary