# Claude Code 系列课程网站

这是一个基于 Flask 的 Claude Code 系列课程网站，提供从安装到高级使用的完整教程。

## 项目结构

```
claude-code-course/
├── app.py                 # Flask 应用主文件
├── requirements.txt       # Python 依赖
├── zeabur_config.yaml    # Zeabur 部署配置
├── Dockerfile            # Docker 配置
├── Procfile              # Heroku 风格的进程文件
├── templates/            # HTML 模板目录
│   ├── index.html        # 主页
│   ├── lesson1.html      # 第一节课：安装环境
│   ├── lesson2.html      # 第二节课：基础使用
│   ├── lesson3.html      # 第三节课：高级用法
│   └── lesson4.html      # 第四节课：实战项目
├── static/               # 静态文件目录
│   ├── style.css         # 样式文件
│   └── script.js         # JavaScript 文件
└── README.md             # 项目说明
```

## 功能特性

- 📚 **完整的课程体系**：从基础安装到高级实战
- 🎨 **现代化设计**：响应式布局，支持多设备访问
- 🚀 **高性能**：基于 Flask 框架，快速稳定
- 📱 **移动端友好**：完全响应式设计

## 本地开发

1. 克隆项目
```bash
git clone <repository-url>
cd claude-code-course
```

2. 创建虚拟环境
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
flask run
```

## 部署到 Zeabur

1. 将项目推送到 Git 仓库
2. 在 Zeabur 控制台创建新项目
3. 选择你的 Git 仓库
4. Zeabur 会自动检测并配置部署

## 部署配置

项目已配置以下文件以支持 Zeabur 部署：

- `requirements.txt` - Python 依赖
- `zeabur_config.yaml` - Zeabur 特定配置
- `Procfile` - 启动命令
- `Dockerfile` - Docker 容器配置

## 环境变量

- `FLASK_ENV` - Flask 环境（development/production）
- `PORT` - 应用端口（默认 5000）

## 技术栈

- **后端**：Flask 2.3.3
- **前端**：HTML5, CSS3, JavaScript
- **部署**：Zeabur, Gunicorn
- **容器化**：Docker

## 许可证

MIT License

## 贡献

欢迎提交 Issues 和 Pull Requests！