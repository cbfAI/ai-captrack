# 本地开发启动指南

由于 Docker Desktop 无法启动，我为您准备了一个不依赖 Docker 的本地开发方案。

## 1. 环境准备

### 1.1 后端依赖

```bash
# 安装 Python 依赖
cd backend
pip install -r requirements.txt
```

### 1.2 前端依赖

```bash
# 安装 Node.js 依赖
cd frontend
npm install
```

## 2. 配置修改

### 2.1 后端配置修改

创建 `backend/.env` 文件：

```env
DATABASE_URL=sqlite:///./aicaptrack.db
REDIS_URL=memory://

HUGGINGFACE_API_URL=https://huggingface.co/api
GITHUB_API_URL=https://api.github.com
FUTURETOOLS_API_URL=https://www.futuretools.io

LLM_API_KEY=your-api-key-here
LLM_API_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4

CACHE_TTL_CAPABILITIES=3600
CACHE_TTL_LLM_PARSE=2592000

SCHEDULER_ENABLED=true
COLLECTION_INTERVAL_HOURS=24
```

### 2.2 后端代码修改

修改 `app/core/config.py` 以支持内存缓存：

```python
# 在 Config 类中添加
REDIS_URL: str = "memory://"
```

修改 `app/services/cache_service.py` 以支持内存缓存：

```python
class CacheService:
    def __init__(self):
        if settings.REDIS_URL.startswith("memory://"):
            self._cache = {}
        else:
            self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.ttl_capabilities = settings.CACHE_TTL_CAPABILITIES
        self.ttl_llm_parse = settings.CACHE_TTL_LLM_PARSE

    def get(self, key: str) -> Optional[Any]:
        if hasattr(self, '_cache'):
            return self._cache.get(key)
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        if hasattr(self, '_cache'):
            self._cache[key] = value
        else:
            self.redis_client.set(key, json.dumps(value), ex=ttl)

    def delete(self, key: str):
        if hasattr(self, '_cache'):
            self._cache.pop(key, None)
        else:
            self.redis_client.delete(key)

    def invalidate_capabilities_cache(self):
        if hasattr(self, '_cache'):
            keys_to_delete = [k for k in self._cache if k.startswith("capabilities:list:")]
            for key in keys_to_delete:
                del self._cache[key]
        else:
            keys = self.redis_client.keys("capabilities:list:*")
            if keys:
                self.redis_client.delete(*keys)
```

## 3. 启动服务

### 3.1 启动后端

```bash
# 在 backend 目录
uvicorn main:app --reload

# 访问：http://localhost:8000
# API 文档：http://localhost:8000/docs
```

### 3.2 启动前端

```bash
# 在 frontend 目录
npm run dev

# 访问：http://localhost:3000
```

## 4. 功能验证

1. **API 文档**：访问 http://localhost:8000/docs 查看 API 接口
2. **前端界面**：访问 http://localhost:3000 查看卡片式界面
3. **数据采集**：点击右上角的"刷新数据"按钮触发采集
4. **筛选功能**：使用左侧筛选栏按类型和 Stars 筛选
5. **用户反馈**：点击卡片上的 👍/👎 进行反馈

## 5. 注意事项

- 由于使用 SQLite 替代 PostgreSQL，部分高级功能可能受限
- 由于使用内存缓存替代 Redis，重启服务后缓存会丢失
- 首次启动时可能需要一些时间来采集数据
- LLM 解析功能需要配置有效的 API Key

## 6. 故障排查

### 6.1 后端启动失败
- 检查端口 8000 是否被占用
- 检查 Python 依赖是否安装成功
- 检查 `.env` 文件配置是否正确

### 6.2 前端启动失败
- 检查端口 3000 是否被占用
- 检查 Node.js 依赖是否安装成功
- 检查网络连接是否正常

### 6.3 数据采集失败
- 检查网络连接是否正常
- 检查 API 速率限制
- 查看后端日志了解具体错误

## 7. 后续步骤

1. **Docker 环境修复**：
   - 重新安装 Docker Desktop
   - 检查系统权限和虚拟化设置
   - 重启计算机

2. **部署到生产环境**：
   - 修复 Docker 环境后，使用 `docker compose up -d` 启动
   - 配置生产环境变量
   - 配置 Nginx 反向代理

3. **功能扩展**：
   - 添加更多数据源
   - 实现定时采集任务
   - 优化 LLM 解析结果
   - 添加用户认证系统
