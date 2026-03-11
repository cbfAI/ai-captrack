# AI CapTrack 开发任务清单

> 最后更新: 2026-03-09

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
