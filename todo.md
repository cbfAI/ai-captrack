# AI CapTrack 开发任务清单

> 最后更新: 2026-03-12

## 进行中的任务

### 1. 智能解析模块优化
**状态**: [x] 已完成

**任务描述**:
- [x] 在采集流程中接入 LLM 智能解析服务
- [x] 解析 AI 能力的关键特性 (key_features)
- [x] 提取解决的痛点 (pain_points)
- [x] 分析与现有方案的区别 (differentiation)
- [x] 实现解析结果缓存机制 (内存缓存，TTL 30天)
- [x] 支持 OpenRouter/GitHub/HuggingFace 多源解析
- [x] 添加解析失败降级处理
- [x] **新增**: 描述内容自动翻译为中文
  - 检测原始语言（中文字符占比 > 30% 视为中文）
  - 非中文内容自动调用 LLM 翻译
  - 翻译结果缓存，避免重复请求
  - 翻译失败时保留原文

**相关文件**:
- `backend/app/services/llm_service.py`
- `backend/app/services/collector_service.py`
- `backend/app/scrapers/*.py`

**预期效果**:
采集的数据自动包含智能分析结果，用户可直观了解每个 AI 能力的价值和适用场景。

---

### 2. 热度评估算法优化
**状态**: [x] 已完成

**任务描述**:
- [x] 设计多维度热度评估模型
  - [x] 基础指标: GitHub Stars / HuggingFace Downloads / OpenRouter 使用量
  - [x] 时间衰减因子: 近期活跃度权重更高（90天半衰期）
  - [x] 社区反馈: 用户点赞/点踩影响热度
  - [x] 来源权重: 不同数据源的可信度差异 (github: 1.0, huggingface: 0.9, openrouter: 0.8)
- [x] 实现热度分数实时更新
- [x] 添加热度趋势计算（上升/下降/稳定）
- [x] 支持自定义热度权重配置 (HeatScoreConfig)
- [x] 编写热度算法单元测试 (31个测试用例全部通过)

**新增字段**:
- `heat_trend`: 热度趋势 (rising/stable/declining)
- `previous_heat_score`: 上次热度分数
- `thumbs_up`: 点赞数
- `thumbs_down`: 点踩数

**相关文件**:
- `backend/app/services/heat_score_service.py` (新建)
- `backend/app/services/capability_service.py`
- `backend/app/models/models.py`

**算法设计草案**:
```
heat_score = base_score * time_decay * source_weight + feedback_bonus

其中:
- base_score: 基础分数 (stars/downloads)
- time_decay: 时间衰减因子 (0.5 ~ 1.0)
- source_weight: 来源权重 (github: 1.0, huggingface: 0.9, openrouter: 0.8)
- feedback_bonus: 反馈加成 (thumbs_up * 10 - thumbs_down * 5)
```

---

## 已完成的任务

### 数据源采集优化
**状态**: [x] 已完成

- [x] 启用 GitHub Trending 采集器
- [x] 新增 OpenRouter 数据源 (346 个 LLM 模型)
- [x] 修复 GitHub 采集器空指针 bug
- [x] 添加 OpenRouter 数据源类型到前后端

### 项目基础设施
**状态**: [x] 已完成

- [x] 配置 SQLite 本地数据库
- [x] 配置内存缓存替代 Redis
- [x] 创建启动脚本

---

## 待规划的任务

### 3. API 排序功能实现
**状态**: [x] 已完成

- [x] 后端支持 sort 参数排序
- [x] 支持多种排序方式 (stars/heat/name/created_at/updated_at)
- [x] 前后端联调

**实现详情**:
- 新增 `SortBy` 枚举: `stars`, `heat`, `name`, `created_at`, `updated_at`
- 新增 `SortOrder` 枚举: `asc`, `desc`
- 默认按热度降序排列
- 前端FilterBar支持8种排序选项

### 4. 集成测试
**状态**: [x] 已完成

**测试文件**:
- `backend/tests/test_scrapers.py` - 采集器单元测试
- `backend/tests/test_api.py` - API端点测试
- `frontend/src/components/__tests__/` - 组件测试

**测试覆盖**:
- [x] 采集器解析逻辑测试
- [x] API CRUD操作测试
- [x] 参数验证测试
- [x] 前端组件测试

**测试运行方式**:
```bash
# 后端测试
cd backend && pytest tests/ -v

# 前端测试
cd frontend && npm test
```

**文档**: 详见 `TESTING.md`

---

## 🔴 优先处理任务

### 5. 收藏功能 API 实现
**状态**: [x] 已完成

**背景**: 前端已调用收藏相关 API，但后端未实现对应接口

**任务描述**:
- [x] 创建收藏 API 路由 (`/api/v1/favorites`)
  - [x] POST `/favorites` - 添加收藏
  - [x] DELETE `/favorites/{capability_id}` - 取消收藏
  - [x] GET `/favorites` - 获取收藏列表
  - [x] GET `/statistics` - 统计数据
- [x] 注册路由到主应用
- [x] 添加前端收藏 hooks (useFavorites, useAddFavorite, useRemoveFavorite, useIsFavorite)
- [x] CapabilityCard 组件添加收藏按钮
- [x] DetailModal 组件添加收藏按钮
- [x] 前后端联调测试

**相关文件**:
- `backend/app/api/favorites.py` (已存在)
- `backend/app/api/__init__.py` (已注册)
- `frontend/src/hooks/useApi.ts` (新增 hooks)
- `frontend/src/components/CapabilityCard.tsx` (添加收藏按钮)
- `frontend/src/components/DetailModal.tsx` (添加收藏按钮)

---

### 6. CI/CD 配置
**状态**: [x] 已完成

**任务描述**:
- [x] 创建 GitHub Actions 工作流
  - [x] 后端测试自动化 (pytest)
  - [x] 前端测试自动化 (vitest)
  - [x] 代码风格检查 (eslint, ruff)
- [x] Docker 镜像构建与推送
- [x] 自动部署配置（可选）

**相关文件**:
- `.github/workflows/ci.yml` (新建)
- `.github/workflows/deploy.yml` (新建)

**CI/CD 配置**:
- 支持分支: `main` 和 `feature/*`
- 自动化测试: 后端 (pytest) + 前端 (vitest)
- 代码风格检查: 后端 (ruff) + 前端 (eslint)
- Docker 镜像: 自动构建并推送到 Docker Hub (主分支)
- 部署流程: 主分支自动部署（需配置部署命令）

---

### 7. 全局异常处理
**状态**: [x] 已完成

**任务描述**:
- [x] 创建统一错误响应格式
- [x] 添加全局异常处理器
  - [x] HTTPException 处理
  - [x] SQLAlchemy 异常处理
  - [x] 通用异常处理
- [x] 添加结构化日志
- [x] 请求追踪 ID 支持

**实现详情**:
- 新增 `ErrorResponse` 类：统一错误响应格式
- 新增自定义异常类：`BaseAPIException`, `ResourceNotFoundError`, `ValidationError`, `AuthenticationError`, `AuthorizationError`, `RateLimitError`, `ExternalServiceError`, `DatabaseError`
- 新增异常处理器：HTTPException、RequestValidationError、SQLAlchemy、BaseAPIException、通用异常
- 新增结构化日志：`StructuredFormatter`, `FormattedStructuredFormatter`, `ColoredFormatter`
- 新增请求追踪中间件：`RequestIDMiddleware`, `LoggingMiddleware`
- 新增 `setup_logging` 函数：配置日志系统
- 新增 `get_logger` 函数：获取日志记录器
- 新增 `log_request` 函数：记录 HTTP 请求日志
- 新增 `log_function_call` 函数：记录函数调用日志

**新增文件**:
- `backend/app/core/exceptions.py`
- `backend/app/core/logging.py`
- `backend/app/core/middleware.py`
- `backend/main.py` (修改)

---

### 8. 数据库迁移脚本
**状态**: [ ] 待开始

**任务描述**:
- [ ] 初始化 Alembic
- [ ] 生成初始迁移脚本
- [ ] 更新 README 部署说明
- [ ] 测试迁移流程

**相关文件**:
- `backend/alembic.ini` (新建)
- `backend/alembic/` (新建目录)

---

### 9. API 认证与限流
**状态**: [ ] 待开始

**任务描述**:
- [ ] JWT 认证实现
  - [ ] 用户注册/登录 API
  - [ ] Token 生成与验证
  - [ ] 保护管理接口
- [ ] API 限流
  - [ ] 集成 slowapi 或自定义限流
  - [ ] 配置限流规则
- [ ] 更新 CORS 配置（生产环境）

**相关文件**:
- `backend/app/core/auth.py` (新建)
- `backend/app/api/auth.py` (新建)
- `backend/app/core/config.py` (修改)
