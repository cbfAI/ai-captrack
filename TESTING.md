# 测试运行指南

## 后端测试

### 热度算法测试（已验证）
```bash
cd backend
python -m pytest tests/test_heat_score.py -v
```
**结果**: 31个测试全部通过 ✓

### 采集器测试
```bash
cd backend
python -m pytest tests/test_scrapers.py -v
```
**覆盖**:
- BaseScraper抽象类测试
- GitHubScraper解析逻辑（类型检测、字段处理、错误处理）
- HuggingFace/OpenRouter基础测试

### API端点测试
```bash
cd backend
python -m pytest tests/test_api.py -v
```
**覆盖**:
- 健康检查端点 (`/`, `/health`)
- 能力管理CRUD操作
- 反馈提交功能
- 分页和排序参数
- 参数验证

## 前端测试

### 安装测试依赖
```bash
cd frontend
npm install
```

### 运行测试
```bash
npm test
```

### 测试覆盖
- `CapabilityCard.test.tsx` - 卡片组件测试
- `FilterBar.test.tsx` - 筛选组件测试
- `Header.test.tsx` - 头部组件测试
- `Pagination.test.tsx` - 分页组件测试

## 测试文件结构

```
backend/tests/
├── test_heat_score.py      # 热度算法（31个测试）
├── test_scrapers.py       # 采集器单元测试
└── test_api.py            # API端点测试

frontend/src/components/__tests__/
├── CapabilityCard.test.tsx
├── FilterBar.test.tsx
├── Header.test.tsx
└── Pagination.test.tsx
```

## 已知问题

1. 采集器异步测试需要pytest-asyncio配置
2. API测试需要数据库隔离设置
3. 前端测试需要安装@testing-library相关包

## CI/CD集成建议

```yaml
# GitHub Actions示例
- name: Run Backend Tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest tests/ -v

- name: Run Frontend Tests  
  run: |
    cd frontend
    npm install
    npm test
```
