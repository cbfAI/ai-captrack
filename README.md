# AI CapTrack - AI 能力追踪平台

> 自动发现、解析、评估最新 AI 模型/技能/工具，回答"有什么新能力？它带来什么变化？我该用吗？"

## 项目简介

AI CapTrack 是一个 AI 能力追踪平台，通过自动采集多个数据源（HuggingFace、GitHub Trending、FutureTools.io）的最新 AI 模型、工具和 Agent 信息，经过智能解析和热度评估后，以卡片式界面呈现给用户。

## 功能特性

- **自动采集**: 从 HuggingFace、GitHub Trending、FutureTools.io 自动抓取最新 AI 资讯
- **智能解析**: 使用 LLM 提取关键信息（是否开源、解决痛点、差异化特点）
- **热度评估**: 基于 GitHub Stars 和社区讨论计算热度分
- **去重合并**: 同一能力在多源出现时自动合并
- **类型筛选**: 支持 Agent / Code / Model 三种类型筛选
- **用户反馈**: 支持 👍/👎 反馈，用于个性化推荐

## 技术栈

### 后端
- **FastAPI** - 高性能 Web 框架，自动生成 API 文档
- **SQLAlchemy** - Python ORM
- **PostgreSQL** - 主数据库
- **Redis** - 缓存层
- **APScheduler** - 定时任务调度
- **httpx** - 异步 HTTP 客户端

### 前端
- **React 18** - UI 框架
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架
- **React Query** - 服务端状态管理
- **Axios** - HTTP 客户端

## 项目结构

```
AICapTrack/
├── backend/
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── db/           # 数据库连接
│   │   ├── models/       # SQLAlchemy 模型
│   │   ├── schemas/      # Pydantic 模型
│   │   ├── services/     # 业务逻辑
│   │   └── scrapers/     # 数据采集器
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/   # UI 组件
│   │   ├── pages/        # 页面
│   │   ├── services/     # API 服务
│   │   ├── hooks/        # 自定义 Hooks
│   │   └── types/        # 类型定义
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 快速开始

### 环境要求

- Docker 和 Docker Compose
- Node.js 18+ (本地开发)
- Python 3.11+ (本地开发)

### Docker 部署

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/AICapTrack.git
cd AICapTrack

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 文件，填入必要的配置（如 LLM API Key）

# 3. 启动所有服务
docker-compose up -d

# 4. 访问应用
# 前端: http://localhost:3000
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 本地开发

#### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

## API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/capabilities` | 获取 AI 能力列表 |
| GET | `/api/v1/capabilities/{id}` | 获取能力详情 |
| POST | `/api/v1/capabilities/{id}/feedback` | 提交用户反馈 |
| GET | `/api/v1/capabilities/filter` | 筛选能力 |
| POST | `/api/v1/collect/trigger` | 手动触发采集 |

## 数据采集源

| 数据源 | 采集内容 | 频率 |
|--------|----------|------|
| HuggingFace | 新模型发布 | 每日 |
| GitHub Trending | 热门 AI 仓库 | 每日 |
| FutureTools.io | AI 工具列表 | 每日 |

## 环境变量

在 `backend/.env` 中配置以下变量：

```env
# 数据库
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aicaptrack

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM API (可选，用于智能解析)
LLM_API_KEY=your_api_key
LLM_API_BASE=https://api.openai.com/v1
```

## 开发进度

- [x] 项目结构初始化
- [x] Docker Compose 环境搭建
- [x] 数据库模型创建
- [x] 数据采集模块
- [x] 智能解析模块
- [x] 热度评估模块
- [x] 去重合并模块
- [x] API 端点开发
- [x] 前端界面开发
- [x] 用户反馈功能
- [x] 缓存机制实现
- [ ] 集成测试
- [ ] 部署验证

## 许可证

MIT License

## 贡献指南

欢迎贡献 AI CapTrack 项目！请遵循以下步骤：

### 开发环境设置

1. Fork 本仓库
2. 克隆你的 Fork：`git clone https://github.com/YOUR_USERNAME/AICapTrack.git`
3. 创建功能分支：`git checkout -b feature/your-feature`

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 代码重构

### Pull Request 流程

1. 确保代码符合项目规范
2. 运行测试（如果有）
3. 提交你的更改
4. 推送分支到你的 Fork
5. 创建 Pull Request 到主仓库

### 联系方式

- 问题反馈：https://github.com/cbfAI/ai-captrack/issues
- 讨论交流：欢迎提交 Issue 和 Pull Request！

---

<p align="center">Made with ❤️ by AI CapTrack Team</p>
