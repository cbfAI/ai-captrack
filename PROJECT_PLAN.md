# AI CapTrack 项目实施计划

## 1. 项目概述

**项目名称**: AI CapTrack - AI 能力追踪平台

**项目目标**: 自动发现、解析、评估最新 AI 模型/技能/工具，回答"有什么新能力？它带来什么变化？我该用吗？"

**技术栈**:
- 后端: Python + FastAPI
- 前端: React + Tailwind CSS
- 数据库: PostgreSQL
- 部署: Docker Compose

---

## 2. 功能需求详细分析

### 2.1 自动采集模块
- **Hugging Face**: 抓取新发布的模型
- **GitHub Trending**: 抓取热门 AI 仓库
- **FutureTools.io**: 抓取 AI 工具列表

### 2.2 智能解析模块
- 使用 AI 提取关键信息：
  - 是否开源
  - 解决什么痛点
  - 与现有方案有何不同

### 2.3 热度评估模块
- 基于 GitHub Stars 计算热度分
- 整合社区讨论数据

### 2.4 去重合并模块
- 同一能力在多源出现时自动合并

### 2.5 Web 展示模块
- 卡片式界面
- 支持按类型筛选（Agent / Code / Model）

### 2.6 用户反馈模块
- 支持 👍/👎 反馈
- 用于个性化推荐

---

## 3. 任务分解与时间规划

### 阶段一：基础设施搭建 (第1-3天)

| 任务 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| T1.1 | 初始化项目结构，创建目录 | 高 | ✅ 完成 |
| T1.2 | 搭建 FastAPI 后端基础框架 | 高 | ✅ 完成 |
| T1.3 | 搭建 React + Tailwind 前端框架 | 高 | ✅ 完成 |
| T1.4 | 配置 PostgreSQL 数据库 | 高 | ✅ 完成 |
| T1.5 | 配置 Docker Compose | 高 | ✅ 完成 |
| T1.6 | 设置数据库模型和迁移 | 高 | ✅ 完成 |

### 阶段二：核心后端开发 (第4-10天)

| 任务 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| T2.1 | 实现数据采集器基类 | 高 | ✅ 完成 |
| T2.2 | 实现 HuggingFace 采集器 | 中 | ✅ 完成 |
| T2.3 | 实现 GitHub Trending 采集器 | 中 | ✅ 完成 |
| T2.4 | 实现 FutureTools 采集器 | 中 | ✅ 完成 |
| T2.5 | 实现智能解析模块（LLM集成） | 高 | ✅ 完成 |
| T2.6 | 实现热度评估模块 | 中 | ✅ 完成 |
| T2.7 | 实现去重合并模块 | 中 | ✅ 完成 |
| T2.8 | 实现缓存机制 | 中 | ✅ 完成 |

### 阶段三：API 开发 (第11-14天)

| 任务 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| T3.1 | 开发 AI 能力列表 API | 高 | ✅ 完成 |
| T3.2 | 开发筛选/搜索 API | 高 | ✅ 完成 |
| T3.3 | 开发用户反馈 API | 中 | ✅ 完成 |
| T3.4 | 开发热度更新定时任务 | 中 | ✅ 完成 |

### 阶段四：前端开发 (第15-21天)

| 任务 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| T4.1 | 开发首页卡片展示组件 | 高 | ✅ 完成 |
| T4.2 | 开发筛选功能（Agent/Code/Model） | 高 | ✅ 完成 |
| T4.3 | 开发详情页 | 中 | 待开发 |
| T4.4 | 开发用户反馈组件 | 中 | ✅ 完成 |
| T4.5 | 实现响应式布局 | 中 | ✅ 完成 |

### 阶段五：集成与部署 (第22-25天)

| 任务 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| T5.1 | 前后端联调 | 高 | 待完成 |
| T5.2 | Docker Compose 优化 | 高 | ✅ 完成 |
| T5.3 | 性能测试 | 中 | 待完成 |
| T5.4 | 部署验证 | 高 | 待完成 |

---

## 4. 技术选型详细说明

### 4.1 后端技术选型

| 组件 | 技术选型 | 理由 |
|------|----------|------|
| Web 框架 | FastAPI | 高性能、自动生成API文档 |
| ORM | SQLAlchemy | Python 主流 ORM |
| 数据库 | PostgreSQL | 支持复杂查询、JSON类型 |
| 缓存 | Redis | 高性能缓存、支持过期策略 |
| HTTP 客户端 | httpx | 异步 HTTP 请求 |
| 定时任务 | APScheduler | Python 定时任务调度 |
| LLM 集成 | 原生 API 调用 | 统一 LLM 调用接口 |

### 4.2 前端技术选型

| 组件 | 技术选型 | 理由 |
|------|----------|------|
| 框架 | React 18 | 主流前端框架 |
| 构建工具 | Vite | 快速开发体验 |
| UI 框架 | Tailwind CSS | 快速样式开发 |
| HTTP 客户端 | Axios | 简洁易用 |
| 状态管理 | React Query | 服务端状态管理 |

### 4.3 数据采集源

| 数据源 | 采集内容 | 频率 |
|--------|----------|------|
| HuggingFace | 新模型发布 | 每日 |
| GitHub Trending | 热门 AI 仓库 | 每日 |
| FutureTools.io | AI 工具列表 | 每日 |

---

## 5. 数据库设计

### 5.1 核心表结构

```
ai_capabilities
├── id: UUID (主键)
├── name: VARCHAR(255) - 名称
├── description: TEXT - 描述
├── capability_type: ENUM(Agent, Code, Model) - 类型
├── source: VARCHAR(50) - 来源
├── source_url: VARCHAR(500) - 原文链接
├── is_open_source: BOOLEAN - 是否开源
├── key_features: JSON - 关键特性
├── pain_points: JSON - 解决的痛点
├── differentiation: TEXT - 与现有方案的区别
├── stars: INTEGER - GitHub 星数
├── heat_score: FLOAT - 热度分
├── metadata: JSON - 原始元数据
├── created_at: TIMESTAMP
├── updated_at: TIMESTAMP

user_feedbacks
├── id: UUID (主键)
├── capability_id: UUID (外键)
├── feedback_type: ENUM(thumbs_up, thumbs_down)
├── created_at: TIMESTAMP
```

---

## 6. API 设计

### 6.1 API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/capabilities | 获取 AI 能力列表 |
| GET | /api/v1/capabilities/{id} | 获取能力详情 |
| POST | /api/v1/capabilities/{id}/feedback | 提交用户反馈 |
| GET | /api/v1/capabilities/filter | 筛选能力 |
| POST | /api/v1/collect/trigger | 手动触发采集 |

### 6.2 请求/响应示例

**GET /api/v1/capabilities**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "filters": {
    "type": "Agent",
    "min_stars": 100
  }
}
```

---

## 7. 缓存策略

### 7.1 缓存内容

| 缓存键 | 内容 | 过期时间 |
|--------|------|----------|
| capabilities:list | 能力列表 | 1 小时 |
| capabilities:{id} | 能力详情 | 24 小时 |
| llm:parse:{hash} | LLM 解析结果 | 30 天 |

### 7.2 成本控制策略

1. **LLM 响应缓存**: 相同内容的解析结果缓存 30 天
2. **数据源缓存**: 采集的数据缓存 1 小时
3. **去重策略**: 采集前检查是否已存在

---

## 8. 项目目录结构

```
AICapTrack/
├── backend/
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── db/           # 数据库
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic 模型
│   │   ├── services/     # 业务逻辑
│   │   └── scrapers/     # 数据采集器
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/   # 组件
│   │   ├── pages/        # 页面
│   │   ├── services/     # API 服务
│   │   ├── hooks/        # 自定义 Hooks
│   │   └── types/        # 类型定义
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
└── README.md
```

---

## 9. 实施检查清单

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

---

## 10. 启动指南

### 10.1 环境要求

- Docker 和 Docker Compose
- Node.js 18+ (本地开发)
- Python 3.11+ (本地开发)

### 10.2 快速启动

```bash
# 1. 克隆项目后，进入目录
cd AICapTrack

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 文件，填入必要的配置

# 3. 启动所有服务
docker-compose up -d

# 4. 访问应用
# 前端: http://localhost:3000
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 10.3 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 前端
cd frontend
npm install
npm run dev
```
