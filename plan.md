目标：自动发现、解析、评估最新 AI 模型/技能/工具，回答“有什么新能力？它带来什么变化？我该用吗？”
1. 功能需求
自动采集：从 Hugging Face、GitHub Trending、FutureTools.io 等源抓取新 AI 能力。
智能解析：用 AI 提取关键信息：是否开源？解决什么痛点？与现有方案有何不同？
热度评估：基于 GitHub Stars、社区讨论等计算热度分。
去重合并：同一能力在多源出现时自动合并。
Web 展示：卡片式界面，支持按类型（Agent / Code / Model）筛选。
用户反馈：支持 👍/👎，用于个性化推荐。
2. 非功能需求
技术栈：Python + FastAPI（后端），React + Tailwind（前端），PostgreSQL（数据库）
部署：支持 Docker Compose 一键启动
成本控制：缓存已解析内容，避免重复调用 LLM
