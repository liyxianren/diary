# 🧠 CBT情绪日记游戏

<div align="center">

![CBT情绪日记游戏](https://img.shields.io/badge/CBT-情绪日记游戏-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-2.3.0-red?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql)
![AI](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)
![Stage](https://img.shields.io/badge/Stage-1%20Completed-brightgreen?style=for-the-badge)

**基于Cursor AI构建的认知行为疗法情绪日记游戏网站**

[项目介绍](#项目简介) • [功能特色](#功能特色) • [快速开始](#快速开始) • [文档](#文档) • [贡献](#贡献)

</div>

## 📖 项目简介

CBT情绪日记游戏是一个融合**认知行为疗法(CBT)**理论与**游戏化交互**的创新Web应用。项目旨在通过**"情绪记录 → 游戏化反馈 → 认知调整"**的闭环系统，帮助用户在轻松游戏的过程中学习和实践CBT技巧，实现情绪管理和心理健康提升。

### 🎯 核心理念

> **影响我们情绪的不是事件本身，而是我们对事件的解读和认知。**

基于CBT理论的认知三角模型，我们通过AI技术分析用户的情绪日记，实时调整游戏体验，让用户在游戏中不知不觉地进行认知重构练习。

### 🔄 技术创新

- **AI深度辅助开发**：全程使用Cursor AI进行智能代码生成和优化
- **情绪数据同步**：日记情绪分析结果实时映射到游戏参数
- **CBT游戏化**：将传统CBT四步法转化为有趣的小游戏
- **个性化体验**：基于用户情绪状态动态调整游戏难度和内容

### 🌟 项目愿景

我们致力于将专业心理健康知识与现代科技结合，让心理治疗变得更加有趣、易得和有效，帮助用户：
- 🎯 **识别情绪模式** - 了解自己的情绪变化规律
- 🧠 **学习认知技巧** - 掌握CBT思维重构方法
- 🎮 **游戏化练习** - 在游戏中培养积极思维习惯
- 📈 **持续改善** - 追踪情绪管理进步轨迹

## ✨ 功能特色

### 🎮 游戏化CBT体验
- **情绪怪兽养成**：根据情绪状态生成个性化游戏角色
- **认知挑战任务**：游戏化实现CBT思维重构练习
- **难度自适应**：基于情绪分析结果动态调整游戏难度
- **成就系统**：通过游戏奖励激励持续的情绪管理练习

### 🤖 AI智能分析
- **多维度情绪识别**：识别6大类基本情绪及其强度
- **认知偏差检测**：自动识别非理性思维模式
- **个性化建议**：基于AI分析生成认知调整建议
- **趋势分析**：追踪情绪变化模式和成长轨迹

### 💻 现代化Web体验
- **响应式设计**：完美适配桌面和移动设备
- **流畅动画**：精心设计的交互效果和微动画
- **实时同步**：前后端数据无缝同步
- **安全可靠**：企业级安全保障和隐私保护

### 🎯 项目目标

- **情绪管理**：帮助用户识别、理解和管理工作情绪
- **认知调整**：通过CBT四步法游戏化实现认知重构
- **习惯培养**：建立持续的情绪记录和积极思维习惯
- **科学辅助**：基于心理学理论和AI技术的科学方法

## 🛠️ 技术栈

### 后端技术
- **框架**: Flask 2.3.3
- **数据库**: MySQL 8.0 (Zeabur云端数据库)
- **ORM**: SQLAlchemy 2.0.36
- **认证**: Flask-JWT-Extended
- **数据库迁移**: Flask-Migrate
- **跨域**: Flask-CORS

### 前端技术
- **基础**: HTML5 + CSS3 + JavaScript ES6+
- **UI框架**: Bootstrap 5.3.0
- **图标**: Font Awesome 6.4.0
- **字体**: Google Fonts (Inter)
- **图表**: Chart.js (情绪可视化)

### AI集成
- **主模型**: COZE API (情绪分析)
- **备用模型**: QWEN模型 (阿里云)
- **功能**: 情绪识别、关键词提取、CBT建议生成

### 开发工具
- **开发环境**: Python 3.9+
- **包管理**: pip + requirements.txt
- **环境配置**: python-dotenv
- **部署平台**: Zeabur
- **版本控制**: Git

## 🏗️ 项目架构

### 数据库设计

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│     users       │    │ emotion_diaries  │    │ emotion_analysis │
├─────────────────┤    ├──────────────────┤    ├──────────────────┤
│ id (PK)         │    │ id (PK)          │    │ id (PK)          │
│ username        │◄───┤ user_id (FK)     │◄───┤ diary_id (FK)    │
│ email           │    │ content          │    │ overall_emotion  │
│ password_hash   │    │ emotion_tags     │    │ emotion_intensity│
│ created_at      │    │ emotion_score    │    │ emotion_dimensions│
│ is_active       │    │ created_at       │    │ key_words        │
│ reset_token     │    │ analysis_status  │    │ confidence_score │
│ reset_token_exp │    │                  │    │ ai_model_version │
└─────────────────┘    └──────────────────┘    └──────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────┐    ┌──────────────────┐
         │  game_states    │    │ game_progress    │
         ├─────────────────┤    ├──────────────────┤
         │ id (PK)         │    │ id (PK)          │
         │ user_id (FK)    │    │ user_id (FK)     │
         │ current_level   │    │ diary_id (FK)    │
         │ game_difficulty │    │ cbt_step         │
         │ character_stats │    │ evidence_collect │
         │ unlocked_features│   │ alternative_th │
         │ total_play_time │    │ game_rewards     │
         │ last_active     │    │ completed_at     │
         └─────────────────┘    └──────────────────┘
```

### 目录结构

```
diary/
├── app.py                 # 主应用文件
├── config.py             # 配置文件
├── extensions.py         # Flask扩展初始化
├── models.py             # 数据库模型
├── requirements.txt      # Python依赖
├── .env.example         # 环境变量模板
├── zeabur_config.py     # Zeabur部署配置
│
├── routes/              # 路由模块
│   ├── __init__.py     # 路由初始化
│   ├── auth.py         # 用户认证路由
│   ├── diary.py        # 日记管理路由
│   ├── analysis.py     # 情绪分析路由
│   ├── game.py         # 游戏状态路由
│   └── stats.py        # 数据统计路由
│
├── templates/           # HTML模板
│   ├── index.html      # 首页
│   ├── login.html      # 登录页
│   ├── register.html   # 注册页
│   ├── reset_password.html # 密码重置页
│   └── ...             # 其他页面模板
│
├── static/             # 静态资源
│   ├── css/
│   │   └── style.css   # 主样式文件
│   ├── js/
│   │   └── main.js     # 主JavaScript文件
│   └── images/         # 图片资源
│
└── uploads/            # 用户上传文件
```

## 🚀 快速开始

### 环境要求

- Python 3.9+
- MySQL 8.0+ (或使用Zeabur云端数据库)
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/cbt-emotion-diary-game.git
cd cbt-emotion-diary-game
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

5. **数据库初始化**
```bash
# 应用会自动创建数据库表，确保数据库连接配置正确
python app.py
```

6. **启动应用**
```bash
python app.py
```

7. **访问应用**
打开浏览器访问 `http://localhost:5000`

### 环境变量配置

创建 `.env` 文件并配置以下变量：

```bash
# Flask基础配置
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# 数据库配置
DATABASE_URL=postgresql://username:password@localhost:5432/emodiary
# 或使用Zeabur云端数据库
# DATABASE_URL=postgresql://user:password@host:port/database

# JWT认证配置
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES_HOURS=24

# AI服务配置
COZE_API_KEY=your-coze-api-key-here
COZE_BOT_ID=your-coze-bot-id-here
COZE_BASE_URL=https://api.coze.com

QWEN_API_KEY=your-qwen-api-key-here
QWEN_MODEL_NAME=qwen-turbo
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1

# Redis配置（可选）
REDIS_URL=redis://localhost:6379/0

# 文件上传配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=txt,pdf,png,jpg,jpeg,gif
```

## 📖 API文档

### 用户认证接口

#### 用户注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**响应**
```json
{
  "message": "用户注册成功",
  "access_token": "string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "created_at": "2024-01-01T00:00:00Z",
    "is_active": true
  }
}
```

#### 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",  // 支持用户名或邮箱
  "password": "string"
}
```

#### 获取用户信息
```http
GET /api/auth/profile
Authorization: Bearer {token}
```

#### 忘记密码
```http
POST /api/auth/forgot-password
Content-Type: application/json

{
  "email": "string"
}
```

#### 重置密码
```http
POST /api/auth/reset-password
Content-Type: application/json

{
  "reset_token": "string",
  "new_password": "string"
}
```

### 日记管理接口

#### 获取日记列表
```http
GET /api/diary?page=1&limit=10
Authorization: Bearer {token}
```

#### 创建日记
```http
POST /api/diary
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "string",
  "emotion_tags": ["开心", "满足"]
}
```

#### 获取单篇日记
```http
GET /api/diary/{diary_id}
Authorization: Bearer {token}
```

#### 更新日记
```http
PUT /api/diary/{diary_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "string",
  "emotion_tags": ["string"]
}
```

#### 删除日记
```http
DELETE /api/diary/{diary_id}
Authorization: Bearer {token}
```

#### 搜索日记
```http
GET /api/diary/search?keyword=string&emotion_tag=string&date_from=2024-01-01&date_to=2024-01-31
Authorization: Bearer {token}
```

### 情绪分析接口

#### 分析单篇日记
```http
POST /api/analysis/{diary_id}
Authorization: Bearer {token}
```

**响应**
```json
{
  "message": "Emotion analysis completed",
  "analysis": {
    "overall_emotion": "happy",
    "emotion_intensity": 0.8,
    "emotion_dimensions": {
      "valence": 0.7,
      "arousal": 0.6,
      "dominance": 0.8
    },
    "key_words": ["开心", "满足", "成功"],
    "confidence_score": 0.85
  },
  "game_mapping": {
    "difficulty_modifier": 0.8,
    "character_effects": {
      "speed": 1.1,
      "strength": 1.0,
      "intelligence": 1.1
    },
    "scenario_recommendations": ["阳光草原", "彩虹山谷"],
    "cbt_challenges": ["维持积极状态", "分享快乐经验"]
  }
}
```

#### 获取分析结果
```http
GET /api/analysis/{diary_id}
Authorization: Bearer {token}
```

#### 批量分析
```http
POST /api/analysis/batch
Authorization: Bearer {token}
Content-Type: application/json

{
  "diary_ids": [1, 2, 3]
}
```

### 游戏状态接口

#### 获取游戏状态
```http
GET /api/game/state
Authorization: Bearer {token}
```

#### 更新游戏状态
```http
POST /api/game/update
Authorization: Bearer {token}
Content-Type: application/json

{
  "current_level": 2,
  "game_difficulty": 1.2,
  "character_stats": {
    "health": 100,
    "energy": 90,
    "mood": 60
  },
  "unlocked_features": {
    "basic_game": true,
    "advanced_challenges": true
  }
}
```

#### 获取游戏进度
```http
GET /api/game/progress
Authorization: Bearer {token}
```

## 📈 开发阶段

### ✅ 阶段1: 数据库连接和登录注册 (已完成) 🎉
- [x] **MySQL数据库连接配置** - Zeabur云端数据库稳定连接
- [x] **用户认证系统** - 注册/登录/JWT token认证完整实现
- [x] **密码重置功能** - 邮箱验证和Token机制
- [x] **现代化前端页面** - 心理学主题UI，响应式设计
- [x] **表单验证和安全** - 前后端双重验证，密码强度检测
- [x] **用户状态管理** - 记住我功能，登录状态同步

**完成时间**: 2025年11月8日
**质量状态**: 生产就绪，全部测试通过

### 🔄 阶段2: 日记书写页面和详情页面 (下一阶段)
- [ ] 日记CRUD API开发
- [ ] 富文本编辑器实现
- [ ] 情绪标签选择器
- [ ] 日记列表和搜索功能
- [ ] 日记统计和数据分析

**预计时间**: 5小时
**核心目标**: 完整的情绪记录系统

### ⏳ 阶段3: 游戏页面开发 (计划中)
- [ ] Canvas游戏画布实现
- [ ] CBT四步法游戏逻辑
- [ ] 游戏角色和动画系统
- [ ] 游戏交互控制
- [ ] 游戏音效和视觉效果

**预计时间**: 6小时
**核心目标**: 游戏化CBT体验

### ⏳ 阶段4: AI分析集成 (计划中)
- [ ] COZE API客户端集成
- [ ] QWEN模型API集成
- [ ] 情绪分析服务优化
- [ ] 分析结果缓存机制
- [ ] 情绪可视化图表

**预计时间**: 5小时
**核心目标**: AI驱动的情绪智能分析

### ⏳ 阶段5: AI与游戏逻辑关联 (计划中)
- [ ] 情绪-游戏难度映射算法
- [ ] 游戏场景推荐系统
- [ ] CBT挑战任务生成
- [ ] 游戏成就系统
- [ ] 情绪变化趋势分析

**预计时间**: 4小时
**核心目标**: 完整的闭环系统

## 🎮 CBT四步法游戏化

### 认知行为疗法四步法

1. **识别负面思维** 🎯
   - 游戏化：思维侦探游戏
   - 帮助用户识别自动化负面思维

2. **寻找支持证据** 🔍
   - 游戏化：证据收集任务
   - 引导用户寻找支持和反对该思维的真实证据

3. **生成替代思维** 💡
   - 游戏化：思维转换挑战
   - 创造更平衡、现实的替代想法

4. **评估情绪变化** 📈
   - 游戏化：情绪计量仪表盘
   - 跟踪认知重构后的情绪改善

### 游戏化特色

- **个性化难度**：根据情绪状态动态调整游戏难度
- **实时反馈**：情绪分析与游戏状态实时同步
- **成就系统**：完成CBT任务获得游戏成就和奖励
- **社交功能**：分享进步，互相鼓励（可选）

## 🎨 界面设计

### 设计理念

- **心理学色彩**：使用蓝、紫、粉、绿渐变营造平静氛围
- **简洁直观**：清晰的导航和操作流程
- **情感共鸣**：通过色彩和动画传递温暖和希望
- **现代美学**：结合最新UI/UX设计趋势

### 响应式设计

- 📱 **移动端优先**：完美适配手机和平板
- 💻 **桌面端优化**：充分利用大屏幕空间
- 🖥️ **跨浏览器兼容**：支持主流浏览器

## 🧪 测试

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-flask

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_auth.py

# 生成覆盖率报告
pytest --cov=app tests/
```

### 测试覆盖

- 单元测试：模型验证、API接口
- 集成测试：用户流程、数据流
- 前端测试：界面交互、表单验证
- 性能测试：API响应时间、数据库查询

## 📈 部署

### Zeabur部署

1. **准备项目**
```bash
# 确保所有依赖都在requirements.txt中
pip freeze > requirements.txt

# 创建启动脚本
echo "python app.py" > start.sh
chmod +x start.sh
```

2. **配置环境变量**
在Zeabur控制台设置所有必要的环境变量

3. **连接数据库**
使用Zeabur提供的MySQL数据库连接字符串

4. **部署应用**
推送代码到Zeabur，自动部署

### 本地部署

```bash
# 使用Gunicorn生产服务器
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 或使用Docker
docker build -t cbt-diary-game .
docker run -p 5000:5000 cbt-diary-game
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下步骤：

### 开发流程

1. **Fork项目**并创建功能分支
```bash
git checkout -b feature/amazing-feature
```

2. **编写代码**并确保符合代码规范
```bash
# 代码格式化
black *.py
flake8 *.py
```

3. **添加测试**并确保通过
```bash
pytest
```

4. **提交更改**
```bash
git commit -m "Add amazing feature"
```

5. **推送分支**并创建Pull Request

### 代码规范

- **Python**: 遵循PEP 8规范
- **JavaScript**: 使用ES6+语法
- **CSS**: 使用BEM命名规范
- **提交信息**: 使用约定式提交格式

### 提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- **Cursor AI** - 提供AI辅助开发支持
- **COZE** - 提供情绪分析API服务
- **阿里云** - 提供QWEN模型服务
- **Zeabur** - 提供部署平台和数据库服务
- **Bootstrap** - 提供UI框架
- **Font Awesome** - 提供图标资源

## 🎯 项目成果与影响

### 📊 技术成果
- **完整的Web应用**：从零构建的现代化全栈应用
- **AI深度集成**：COZE和QWEN模型的无缝集成
- **创新交互设计**：CBT理论与游戏化的完美结合
- **生产级代码质量**：完整的安全验证和错误处理

### 🌟 社会价值
- **心理健康普及**：让专业心理治疗技术变得更加易得
- **预防性干预**：帮助用户在日常生活中管理情绪
- **科学方法推广**：推广基于证据的心理健康方法
- **技术创新示范**：展示AI在心理健康领域的应用潜力

## 🔮 未来规划

### 短期目标 (3-6个月)
- [ ] 完成阶段2-5的核心功能开发
- [ ] 优化AI分析准确性和响应速度
- [ ] 添加更多情绪标签和CBT技巧
- [ ] 完善用户反馈和迭代机制

### 中期目标 (6-12个月)
- [ ] 开发移动端APP版本
- [ ] 添加社交功能和互助社区
- [ ] 集成更多专业心理健康资源
- [ ] 支持多语言和国际化

### 长期愿景 (1-2年)
- [ ] 建立完整的心理健康生态平台
- [ ] 与专业心理咨询师和机构合作
- [ ] 开展临床效果验证和研究
- [ ] 推广到学校、企业和医疗机构

## 📞 联系我们

### 项目信息
- **项目主页**: [GitHub Repository](https://github.com/your-username/cbt-emotion-diary-game)
- **在线演示**: [https://your-demo-url.com](https://your-demo-url.com)
- **项目文档**: [完整文档](https://your-docs-site.com)

### 联系方式
- **邮箱联系**: your-email@example.com
- **问题反馈**: [GitHub Issues](https://github.com/your-username/cbt-emotion-diary-game/issues)
- **功能建议**: 欢迎通过Issues或邮件提出建议

### 商业合作
- **技术合作**: 寻求AI技术、心理健康领域的合作机会
- **学术研究**: 欢迎心理学、计算机科学领域的学术合作
- **商业应用**: 对企业版、教育版等定制化开发感兴趣

## 🙏 致谢

### 技术支持
- **Cursor AI** - 提供强大的AI辅助开发能力
- **COZE API** - 提供专业的情绪分析服务
- **QWEN模型** - 提供高质量的自然语言处理能力
- **Zeabur平台** - 提供稳定的云端部署服务

### 理论基础
- **认知行为疗法(CBT)** - Aaron T. Beck博士创立的科学心理治疗方法
- **情绪心理学** - Paul Ekman教授的情绪研究理论
- **积极心理学** - Martin Seligman博士的幸福科学研究

### 开源社区
感谢所有为开源项目做出贡献的开发者，特别是：
- **Flask团队** - 优秀的Web框架
- **Bootstrap团队** - 现代化的UI框架
- **开源社区** - 无数开发者的智慧结晶

## 📄 许可证

本项目采用 **MIT 许可证**，您可以在 LICENSE 文件中查看完整的许可条款。简单来说，您可以：
- ✅ 自由使用、复制、修改和分发
- ✅ 用于商业目的
- ✅ 私人使用无需开源
- ⚠️ 需要保留版权声明和许可声明

---

<div align="center">

## 🌟 支持我们

如果这个项目对您有帮助，请考虑：
- **⭐ 给我们一个Star** - 让更多人发现这个项目
- **🐛 报告问题** - 帮助我们改进产品质量
- **💡 提出建议** - 分享您的想法和需求
- **📢 分享给朋友** - 让更多人受益于心理健康科技

**Made with ❤️ and AI by CBT Emotion Diary Game Team**

*用科学与爱，帮助每个人重获内心平衡*

</div>