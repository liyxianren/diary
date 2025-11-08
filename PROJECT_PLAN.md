# CBT情绪日记游戏 - 项目开发计划

## 项目概述
基于Cursor AI构建的CBT情绪日记游戏网站，结合认知行为疗法与游戏化设计，帮助用户管理情绪。

## 技术栈
- **后端**: Flask + MySQL (Zeabur云端数据库)
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap
- **AI集成**: COZE API + QWEN模型
- **部署**: Zeabur平台

## 开发阶段详细计划

### 阶段1: 数据库连接和登录注册开发 (已完成 ✅)

#### 任务清单:

**后端开发 (2小时)**
- [x] 配置MySQL数据库连接 - 使用Zeabur MySQL数据库
- [x] 创建用户数据表结构 - User模型已创建
- [x] 实现用户注册API (`POST /api/auth/register`) - 功能正常
- [x] 实现用户登录API (`POST /api/auth/login`) - 功能正常
- [x] 实现JWT token认证机制 - JWT工作正常
- [x] 密码加密存储 (Werkzeug) - 密码安全加密
- [x] 用户输入验证和数据清洗 - 输入验证已实现

**前端开发 (1.5小时)**
- [x] 创建注册页面 (`/register`) - 页面正常加载
- [x] 创建登录页面 (`/login`) - 页面正常加载
- [x] 表单验证和错误提示 - 完整的前端验证逻辑已实现
- [x] 实现记住我功能 - localStorage/sessionStorage支持已实现
- [x] 添加忘记密码链接 - 完整的密码重置功能已实现

**测试 (0.5小时)**
- [x] 数据库连接测试 - 连接成功
- [x] 用户注册流程测试 - 完整API功能验证通过
- [x] 用户登录流程测试 - 完整API功能验证通过
- [x] JWT token验证测试 - Token认证机制正常工作

#### 技术要点:
```python
# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### API接口文档:
```
【用户认证接口】
1. 用户注册
URL: POST /api/auth/register
参数: {"username": "string", "email": "string", "password": "string"}
返回: {"message": "string", "access_token": "string", "user": {...}}

2. 用户登录 (支持用户名或邮箱)
URL: POST /api/auth/login
参数: {"username": "string", "password": "string"}  // username可以是用户名或邮箱
返回: {"message": "string", "access_token": "string", "user": {...}}

3. 获取用户信息
URL: GET /api/auth/profile
头部: Authorization: Bearer {token}
返回: {"user": {...}}

4. 忘记密码
URL: POST /api/auth/forgot-password
参数: {"email": "string"}
返回: {"message": "string", "reset_token": "string"}

5. 重置密码
URL: POST /api/auth/reset-password
参数: {"reset_token": "string", "new_password": "string"}
返回: {"message": "string"}

6. 健康检查
URL: GET /api/health
返回: {"status": "string", "timestamp": "string", "version": "string"}
```

#### 当前状态:
- ✅ 后端API已搭建完成，可以正常注册和登录
- ✅ 前端页面模板已创建，可以正常访问
- ✅ 完整的用户流程测试已完成 - 所有API功能验证通过
- ✅ 前端JavaScript交互逻辑已完善 - 包含完整的表单验证、记住我、忘记密码功能
- ✅ 用户界面已现代化设计 - 包含心理学主题色彩和动画效果
- ✅ 全部Bug已修复 - 登录状态、中文错误信息、邮箱登录、布局问题

### 阶段2: 日记书写页面和详情页面 (5小时)

#### 任务清单:

**后端开发 (2小时)**
- [ ] 创建日记数据表结构
- [ ] 实现日记CRUD API
  - `GET /api/diary` - 获取日记列表
  - `POST /api/diary` - 创建新日记
  - `GET /api/diary/{id}` - 获取单篇日记
  - `PUT /api/diary/{id}` - 更新日记
  - `DELETE /api/diary/{id}` - 删除日记
- [ ] 实现日记分页和搜索功能
- [ ] 添加日记统计API

**前端开发 (2.5小时)**
- [ ] 创建日记列表页面 (`/diary`)
- [ ] 创建日记编辑页面 (`/diary/new`)
- [ ] 创建日记详情页面 (`/diary/{id}`)
- [ ] 实现富文本编辑器
- [ ] 添加情绪标签选择器
- [ ] 实现日记切换导航
- [ ] 添加日期选择器

**测试 (0.5小时)**
- [ ] 日记CRUD功能测试
- [ ] 页面切换测试
- [ ] 富文本编辑器测试

#### 技术要点:
```javascript
// 日记数据结构
const diary = {
    id: 1,
    content: "今天感觉...",
    emotion_tags: ["开心", "满足"],
    emotion_score: {},
    created_at: "2024-01-01T10:00:00Z",
    analysis_status: "pending"
};
```

### 阶段3: 游戏页面开发 (6小时)

#### 任务清单:

**后端开发 (2小时)**
- [ ] 创建游戏状态数据表
- [ ] 实现游戏状态管理API
  - `GET /api/game/state` - 获取游戏状态
  - `POST /api/game/update` - 更新游戏状态
  - `GET /api/game/progress` - 获取游戏进度
- [ ] 实现游戏难度算法
- [ ] 添加游戏奖励系统

**前端开发 (3.5小时)**
- [ ] 创建游戏主页面 (`/game`)
- [ ] 实现Canvas游戏画布
- [ ] 开发CBT四步法游戏逻辑
- [ ] 添加游戏角色和动画
- [ ] 实现游戏交互控制
- [ ] 添加游戏音效和视觉效果
- [ ] 创建游戏说明和教程

**测试 (0.5小时)**
- [ ] 游戏逻辑测试
- [ ] Canvas渲染测试
- [ ] 游戏状态同步测试

#### 技术要点:
```javascript
// Canvas游戏基础
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // 游戏逻辑
    updateGameState();
    renderGame();
    requestAnimationFrame(gameLoop);
}
```

### 阶段4: AI分析集成 (5小时)

#### 任务清单:

**后端开发 (3小时)**
- [ ] 集成COZE API客户端
- [ ] 集成QWEN模型API
- [ ] 实现情绪分析服务
- [ ] 创建情绪分析API
  - `POST /api/analysis/{diary_id}` - 分析单篇日记
  - `GET /api/analysis/{diary_id}` - 获取分析结果
  - `POST /api/analysis/batch` - 批量分析
- [ ] 添加分析结果缓存机制
- [ ] 实现关键词提取功能

**前端开发 (1.5小时)**
- [ ] 创建分析结果展示组件
- [ ] 添加分析进度指示器
- [ ] 实现情绪可视化图表
- [ ] 添加分析历史记录页面

**测试 (0.5小时)**
- [ ] AI API调用测试
- [ ] 分析结果准确性测试
- [ ] 性能优化测试

#### 技术要点:
```python
# 情绪分析服务
class EmotionAnalysisService:
    def analyze_with_coze(self, text):
        # COZE API集成
        pass

    def analyze_with_qwen(self, text):
        # QWEN模型集成
        pass
```

### 阶段5: AI分析与游戏逻辑关联 (4小时)

#### 任务清单:

**后端开发 (2小时)**
- [ ] 实现情绪-游戏难度映射算法
- [ ] 创建游戏场景推荐系统
- [ ] 实现CBT挑战任务生成
- [ ] 添加游戏状态实时更新
- [ ] 实现情绪变化趋势分析

**前端开发 (1.5小时)**
- [ ] 实现游戏难度动态调整
- [ ] 添加情绪变化可视化
- [ ] 创建游戏推荐界面
- [ ] 实现CBT任务引导
- [ ] 添加游戏成就系统

**测试 (0.5小时)**
- [ ] 情绪-游戏映射测试
- [ ] 游戏难度调整测试
- [ ] 整体流程测试

#### 技术要点:
```javascript
// 情绪-游戏映射
function mapEmotionToGame(emotionData) {
    const difficulty = emotionData.intensity * 0.8 + 0.2;
    const characterEffects = generateCharacterEffects(emotionData.emotion);
    return { difficulty, characterEffects };
}
```

## 数据库设计

### 核心数据表

1. **users** - 用户表 ✅ 已实现
   - id, username, email, password_hash, created_at
   - reset_token, reset_token_expires (密码重置功能)
2. **emotion_diaries** - 情绪日记表
3. **emotion_analysis** - 情绪分析结果表
4. **game_states** - 游戏状态表
5. **game_progress** - 游戏进度表

### 数据库连接配置
```
DATABASE_URL=mysql+pymysql://root:q37sTw1xgc2h46589NbdZFzMAnPrpEm0@hkg1.clusters.zeabur.com:32570/zeabur
```

## API接口规范

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/profile` - 获取用户信息

### 日记相关
- `GET /api/diary` - 获取日记列表
- `POST /api/diary` - 创建新日记
- `GET /api/diary/{id}` - 获取单篇日记
- `PUT /api/diary/{id}` - 更新日记
- `DELETE /api/diary/{id}` - 删除日记

### 分析相关
- `POST /api/analysis/{diary_id}` - 分析单篇日记
- `GET /api/analysis/{diary_id}` - 获取分析结果

### 游戏相关
- `GET /api/game/state` - 获取游戏状态
- `POST /api/game/update` - 更新游戏状态

## 前端页面结构

```
templates/
├── index.html          # 首页 ✅ 已实现 - 现代化设计，登录状态管理
├── login.html          # 登录页 ✅ 已实现 - 完整表单验证，记住我功能
├── register.html       # 注册页 ✅ 已实现 - 密码强度检测，现代化UI
├── reset_password.html # 密码重置页 ✅ 已实现 - Token验证，密码强度检查
├── diary/
│   ├── list.html       # 日记列表
│   ├── edit.html       # 日记编辑
│   └── detail.html     # 日记详情
└── game/
    ├── index.html      # 游戏主页
    └── tutorial.html   # 游戏教程

static/
├── css/
│   └── style.css       # 样式文件 ✅ 已实现 - 心理学主题色彩，响应式设计
└── js/
    └── main.js         # 公共JS ✅ 已实现 - API调用，表单验证，UI管理
```

## 开发环境配置

### 环境变量 (.env)
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:q37sTw1xgc2h46589NbdZFzMAnPrpEm0@hkg1.clusters.zeabur.com:32570/zeabur
JWT_SECRET_KEY=your-jwt-secret-key-here
COZE_API_KEY=your-coze-api-key-here
COZE_BOT_ID=your-coze-bot-id-here
QWEN_API_KEY=your-qwen-api-key-here
```

### 运行项目
```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 访问网站
http://localhost:5000
```

## 测试计划

### 单元测试
- 数据库模型测试
- API接口测试
- 认证功能测试

### 集成测试
- 用户注册登录流程
- 日记CRUD操作
- 情绪分析流程
- 游戏逻辑测试

### 性能测试
- 数据库查询优化
- API响应时间
- 前端加载速度

## 部署计划

### Zeabur部署步骤
1. 配置环境变量
2. 数据库初始化
3. 代码推送和部署
4. 域名配置
5. SSL证书配置

### 部署检查清单
- [ ] 环境变量配置正确
- [ ] 数据库连接正常
- [ ] API接口测试通过
- [ ] 前端页面加载正常
- [ ] 用户注册登录测试
- [ ] 日记功能测试
- [ ] 游戏功能测试
- [ ] AI分析功能测试

## 时间安排

总开发时间：**24小时**

- 阶段1: 4小时
- 阶段2: 5小时
- 阶段3: 6小时
- 阶段4: 5小时
- 阶段5: 4小时

## 风险评估与应对

### 技术风险
1. **AI API调用失败** - 准备备用分析方案
2. **数据库连接问题** - 本地SQLite备份方案
3. **性能瓶颈** - 缓存机制和代码优化

### 时间风险
1. **功能复杂度超预期** - 简化功能或调整优先级
2. **第三方服务不可用** - 使用模拟数据继续开发

## 项目成功标准

- ✅ 用户注册登录功能正常
- ✅ 日记CRUD功能完整
- ✅ 游戏化CBT体验流畅
- ✅ AI情绪分析准确
- ✅ 情绪-游戏关联逻辑正确
- ✅ Zeabur部署成功
- ✅ 24小时内完成开发

---

## 📊 项目进度更新

**2025年11月8日 - 阶段1完全完成报告**

### ✅ 已完成功能
1. **用户认证系统** - 完全实现并通过测试
   - 用户注册API (`POST /api/auth/register`) - 完整验证，中文错误信息
   - 用户登录API (`POST /api/auth/login`) - 支持用户名/邮箱登录
   - JWT token认证机制 - 完整token管理
   - 获取用户信息API (`GET /api/auth/profile`) - 用户信息获取
   - 健康检查API (`GET /api/health`) - 系统状态监控
   - 忘记密码API (`POST /api/auth/forgot-password`) - 邮箱验证
   - 重置密码API (`POST /api/auth/reset-password`) - Token验证

2. **数据库连接** - 稳定运行
   - Zeabur MySQL数据库连接正常
   - 用户数据表结构完整 (含密码重置字段)
   - 数据持久化和查询功能正常
   - 自动数据库升级功能已实现

3. **前端页面** - 现代化完整实现
   - 主页 (`/`) - Hero区域，功能介绍，登录状态管理
   - 登录页 (`/login`) - 表单验证，记住我，忘记密码
   - 注册页 (`/register`) - 密码强度检测，实时验证
   - 密码重置页 (`/reset-password`) - Token验证，密码强度

4. **UI/UX设计** - 现代化心理学主题
   - 响应式设计，适配各种设备
   - 心理学色彩主题 (蓝、紫、粉、绿渐变)
   - 流畅动画效果和微交互
   - 完整的错误提示和用户反馈

5. **安全功能** - 完整实现
   - 密码强度验证和加密存储
   - JWT token安全认证
   - 输入数据验证和清洗
   - XSS和注入攻击防护

### 🔧 已修复问题
- **JWT Token认证** - 修复了identity参数类型问题
- **API错误处理** - 完善了各种边界情况处理
- **登录状态管理** - 修复退出后状态显示问题
- **中文错误信息** - 所有错误信息已本地化
- **邮箱登录支持** - 实现用户名/邮箱双重登录方式
- **UI布局问题** - 修复重复图标和布局错误
- **数据库升级** - 实现无停机数据库结构升级

### 📈 技术亮点
- **现代化前端架构** - Bootstrap 5 + 自定义CSS + JavaScript
- **完整的表单验证** - 前端实时验证 + 后端数据验证
- **用户体验优化** - 加载状态，错误提示，成功反馈
- **安全性保障** - 多层安全验证，密码加密，Token管理

### 🎯 下一步计划
**阶段2: 日记书写页面和详情页面** (预计5小时)
- 日记CRUD API开发
- 富文本编辑器实现
- 情绪标签选择器
- 日记列表和详情页面
- 情绪分析集成准备

---

**项目状态**: 阶段1已完成，准备进入阶段2
**最后更新**: 2025年11月8日
**开发团队**: Cursor AI + 开发者协作