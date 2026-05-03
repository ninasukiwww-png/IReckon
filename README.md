# IReckon — 俺寻思 AI 工厂 (๑•́ ∀ •̀๑)

> *"IReckon" — Orkish for "I think it can work"

**IReckon** 是一个敲腻害的**多智能体自主编程系统**喵～ (≧∀≦)ゞ
只需要输入自然语言需求，AI 小伙伴们就会自动帮你完成规划、编码、审查、修改、交付全流程，完全不需要人工干预呢！是不是超级方便呀～ ✨

---

## 🚀 快速开始 (快来玩嘛～)

### 环境要求 (要先准备好哦)

- Python 3.10+ 喵～
- LLM 端点（默认 Ollama `http://localhost:11434` + `qwen2.5:7b`，不会设置的话问问度娘吧～）

### 安装 (安装超简单的！)

```bash
git clone https://github.com/ninasukiwww-png/IReckon.git
cd IReckon
pip install -r requirements.txt
```

### 启动 (biu~ 启动啦！)

```bash
# 方式一：一键启动（后端 + 前端）—— 推荐懒人用法！
bash run.sh

# 方式二：分别启动（了解一下嘛～）
python -m uvicorn app.web.api:app --host 0.0.0.0 --port 8000   # 后端酱～
cd frontend && npm run dev                                       # 前端酱～

# 方式三：启动前检查环境（确认一下没问题喵）
bash run.sh --check
```

启动后就可以玩啦：
- 后端 API: `http://localhost:8000` — Swagger 文档 `/docs`
- 前端 UI: `http://localhost:5173` — Vue3 界面

### 使用流程 (超简单的五步走～)

1. 打开前端 UI，点击 **New Task** ✿
2. 输入自然语言需求，比如 `"创建一个 Flask TODO 应用，支持增删改查"` ✨
3. AI 团队自动执行：规划 → 编码 → 审查 → 修改 → 交付 (≧∇≦)
4. 在 Chat / Dashboard 页面实时查看进度 (实时监控超酷的！)
5. 成品输出到 `data/outputs/{task_id}/` ✧(｡•̀ᴗ-)✧

---

## 🏗️ 架构 (看看就好，别怕～)

```
┌──────────────────────────────────────────────────────────┐
│                   Vue3 Frontend (port 5173)                 │
│   Chat / Dashboard / Config Panel / Theme Selector        │
└────────────────────────┬─────────────────────────────────┘
                          │ HTTP / WebSocket
┌────────────────────────▼─────────────────────────────────┐
│                   FastAPI Backend (port 8000)              │
│   REST API (/api/tasks, /api/ai-instances, /api/config)   │
│   WebSocket (/ws/{task_id})                               │
└────────────────────────┬─────────────────────────────────┘
                          │
┌────────────────────────▼─────────────────────────────────┐
│                    Workflow Engine                         │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│   │ Planning │──▶│ Execute  │──▶│  Review  │              │
│   └──────────┘   └──────────┘   └────┬─────┘              │
│         ▲                            │ pass/fail          │
│         │                   ┌────────▼────────┐            │
│         └───────────────────│  Revise / Deliver│            │
│                             └─────────────────┘            │
└────────────────────────┬─────────────────────────────────┘
                          │
┌────────────────────────▼─────────────────────────────────┐
│                    AI Agent Team                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │Scheduler │ │ Executor │ │ Reviewer │ │Deliverer │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │ Creative │ │ Learner  │ │Tool Mgr  │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
└────────────────────────┬─────────────────────────────────┘
                          │
┌────────────────────────▼─────────────────────────────────┐
│                  Infrastructure                            │
│  LLM Pool (litellm) │ ChromaDB │ SQLite │ Security Suite   │
└──────────────────────────────────────────────────────────┘
```

---

## 🤖 AI 角色 (分工合作效率高！)

| 角色 | 职责 |
|------|------|
| **Scheduler** (调度员酱) | 把需求拆成小任务，给每个阶段找合适的 AI 小伙伴～ |
| **Executor** (开发者酱) | 写代码、打补丁、调试修复，超级能干的！ |
| **Reviewer** (审查员酱) | 正确性审查 + 效率/架构审查，双重把关超严格！ |
| **Deliverer** (交付员酱) | 打包产物、生成 READY.txt、归档输出，完美主义者！ |
| **Creative** (创意官酱) | 头脑风暴、方案设计、技术选型建议，脑洞大开！ |
| **Learner** (学习者酱) | 空闲时爬取 GitHub Trending，学习开源模式，超爱学习的！ |
| **Tool Manager** (工具管理酱) | 管理工具零件库，按需调用内置工具，管家属性！ |

## 🔄 工作流 (循环超有趣的！)

IReckon 用 **LangGraph** 构建敲智能的有向状态图～

```
planning ──▶ execute ──▶ review ──┐
                ▲            │     │
                │      ┌─────┘     │
                │      ▼           ▼
                └── revise     deliver ──▶ END
                                    
                fail ──▶ handle_error ──▶ END
```

- **review_router**: 审查通过 → 交付；需修改 → 修订；失败 → 错误处理
- **revise_router**: 状态为 executing → 继续执行；否则 → 重新审查
- 超过 3 轮修订自动升级到高性能模型（偷懒的最高境界！）

---

## ✨ 特性 (亮点多多！)

### 核心 (最重要的部分！)
- **多角色 AI 团队** — 7 种专业角色协同工作，分工明确！
- **全自动交付** — 提需求 → 出成品，零人工介入，躺平就完事！
- **LangGraph 状态机** — 带条件路由的正式工作流，稳得很！
- **双重审查** — 正确性 + 效率架构双重把关，不放过任何小问题！
- **智能重试** — 审查失败自动修订，超过阈值自动换模型，超智能的！

### LLM 与 AI (AI 大脑超重要！)
- **模型无关** — 通过 litellm 支持 100+ 模型（Ollama / OpenAI / Anthropic / Google / Azure 等）
- **能力池** — 多端点管理、自动故障转移、健康检测、冷却机制
- **流式/非流式** — 自动降级、指数退避重试

### 安全 (安全第一！)
- **代码扫描** — 集成 Bandit / semgrep，坏代码无处遁形！
- **命令分级** — L1 自动执行 / L2 投票阈值 / L3 拦截
- **沙箱执行** — udocker 容器隔离，危险操作也不怕！
- **供应链防火墙** — pip / npm 黑名单过滤，坏东西进不来！
- **挖矿检测** — 进程命令行匹配，守护你的算力！

### 用户体验 (用着超舒服的！)
- **实时推送** — WebSocket 推送进度、日志、消息，随时掌握动态！
- **可定制主题** — catgirl / programmer 角色扮演主题，换装play！
- **任务快照** — 支持暂停 / 恢复，想停就停超自由！
- **配置热重载** — YAML 修改自动生效，改完不用重启！
- **空闲学习** — 无任务时自动学习 GitHub Trending，超爱学习的酱酱！

---

## ⚙️ 配置 (调一调更顺手！)

所有配置集中在 `config/config.yaml`，支持环境变量引用 `${VAR:-default}` 和热重载～

### 核心配置项 (了解一下比较好！)

```yaml
server:
  host: 0.0.0.0       # 服务监听地址
  port: 8000          # 服务端口
  log_level: INFO     # 日志级别

ai_pool:
  default_model: qwen2.5:7b   # 默认 LLM 模型
  instances:                  # AI 端点列表
    - id: local-ollama-qwen
      model: ollama/qwen2.5:7b
      endpoint: http://localhost:11434
      tags: [general, cheap, fast, python]

ui:
  theme: catgirl          # UI 主题（catgirl / programmer / raw）
  default_view: styled    # 默认视图模式

task_defaults:
  max_review_rounds: 5         # 最大审查轮次
  loop_detection_max_rounds: 5  # 循环检测阈值
```

可以在前端 UI 的 Config Panel 实时修改，也可以用 API：

```bash
curl -X POST http://localhost:8000/api/config/update \
  -H "Content-Type: application/json" \
  -d '{"updates": {"ui.theme": "programmer"}}'
```

---

## 📚 API 文档 (码农必备！)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/tasks` | 创建新任务 |
| GET | `/api/tasks` | 列出所有任务 |
| GET | `/api/tasks/{id}` | 获取任务详情 |
| POST | `/api/tasks/{id}/cancel` | 取消任务 |
| POST | `/api/tasks/{id}/resume` | 恢复任务 |
| GET | `/api/tasks/{id}/messages` | 获取任务消息 |
| POST | `/api/tasks/{id}/messages` | 发送消息 |
| GET | `/api/ai-instances` | 列出 AI 端点 |
| POST | `/api/ai-instances` | 创建 AI 端点 |
| PUT | `/api/ai-instances/{id}` | 更新 AI 端点 |
| DELETE | `/api/ai-instances/{id}` | 删除 AI 端点 |
| POST | `/api/ai-instances/{id}/test` | 测试 AI 端点 |
| GET | `/api/config` | 获取配置 |
| POST | `/api/config/update` | 更新配置 |
| GET | `/api/themes` | 获取主题列表 |
| GET | `/api/health` | 健康检查 |
| WS | `/ws/{task_id}` | 任务 WebSocket |
| WS | `/ws` | 全局 WebSocket |

---

## 🛠️ 技术栈 (都是好东西！)

| 模块 | 技术 |
|------|------|
| 语言 | Python 3.10+ (asyncio) |
| LLM 接口 | litellm（100+ 模型） |
| 工作流 | LangGraph |
| 向量数据库 | ChromaDB |
| 关系数据库 | SQLite (aiosqlite) |
| 后端框架 | FastAPI + WebSocket |
| 前端框架 | Vue 3 + Vite |
| 配置管理 | YAML + 环境变量 + watchdog 热重载 |
| 日志 | loguru |
| 安全扫描 | Bandit, semgrep |
| 沙箱 | udocker |
| 加密 | cryptography (Fernet) |
| 模板引擎 | Jinja2 |

---

## 💻 开发 (一起来玩嘛～)

```bash
# 环境检查
python scripts/preflight.sh

# 功能测试（创建 Hello World 任务）
python scripts/test_run.py

# 代码扫描
bandit -r app/
semgrep --config=auto app/
```

### 环境变量 (了解一下不吃亏！)

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `IRECKON_HOME` | `.` | 项目根目录 |
| `IRECKON_API_HOST` | `localhost` | API 主机地址 |
| `IRECKON_API_PORT` | `8000` | API 端口 |
| `IRECKON_API_TIMEOUT` | `10` | API 请求超时（秒） |

---

## 📁 目录结构 (看看都有啥～)

```
IReckon/
├── main.py                    # 应用入口 (程序酱的开始！)
├── run.sh                     # 启动脚本 (一键启动超方便)
├── requirements.txt           # 依赖 ( pip install 就完事 )
├── pyproject.toml             # 项目元数据 ( metadata~ )

├── app/                       # 后端包
│   ├── agents/                # AI 角色实现
│   │   ├── base.py            #   基类 (大家的爸爸！)
│   │   ├── scheduler.py       #   调度员 (分发任务的小天使)
│   │   ├── executor.py        #   开发者 (写代码的超人！)
│   │   ├── reviewer.py        #   审查员 (找茬但为了你好！)
│   │   ├── deliverer.py       #   交付员 (打包小能手)
│   │   ├── creative.py        #   创意官 (脑洞担当！)
│   │   ├── learner.py         #   学习者 (爱学习的乖宝宝)
│   │   ├── tool_manager.py    #   工具管理 (工具人但很重要！)
│   │   └── content_filter.py  #   内容安全过滤 (守护者！)
│   ├── core/                  # 基础设施
│   │   ├── config.py          #   配置管理 (热重载超酷的)
│   │   ├── database.py        #   SQLite + Fernet 加密 (数据保护盾！)
│   │   ├── logger.py          #   loguru 日志 (记录一切！)
│   │   └── state.py           #   任务状态快照 (存档小天才)
│   ├── engine/                # 工作流引擎 (动力源泉！)
│   │   ├── machine.py         #   LangGraph 状态机 (超级大脑)
│   │   ├── tasks.py           #   任务生命周期 (生老病死了解一下)
│   │   ├── room.py            #   会议室 (多 agent 开会地！)
│   │   ├── board.py           #   Kanban 看板 (任务进度一目了然)
│   │   ├── registry.py        #   角色注册表 (身份证登记处)
│   │   ├── detector.py        #   循环检测 (死循环退退退！)
│   │   ├── cost.py            #   成本追踪 (算账小能手)
│   │   ├── learner.py         #   空闲学习循环 (爱学习的酱酱)
│   │   └── style.py           #   UI 主题引擎 (换装play！)
│   ├── llm/                   # LLM 层 (AI 大脑！)
│   │   ├── client.py          #   客户端 (重试/回退/流式全都会)
│   │   └── pool.py            #   能力池 (端点管理大师)
│   ├── knowledge/             # 知识库 (AI 的小脑瓜)
│   │   ├── vector.py          #   ChromaDB 向量库 (存记忆的地方)
│   │   └── files.py           #   文件知识库 (资料库！)
│   ├── security/              # 安全子系统 (保安团！
│   │   ├── scanner.py         #   代码扫描 (找虫虫！)
│   │   ├── filter.py          #   命令分级过滤 (分级管理)
│   │   ├── sandbox.py         #   udocker 沙箱 (安全隔离屋)
│   │   ├── mining.py          #   挖矿检测 (赶走挖矿怪！)
│   │   └── supply.py          #   供应链防火墙 (守住大门！)
│   ├── tools/                 # 工具系统 (百宝箱！)
│   │   ├── registry.py        #   工具注册 (登记处)
│   │   ├── library.py         #   零件库 (零件大仓库)
│   │   ├── assembler.py      #   工具组装器 (组装大师！)
│   │   └── builtin/           #   内置工具 (自带的宝藏)
│   └── web/                   # Web 层 (网络接口！)
│       ├── api.py             #   FastAPI 路由 (路由小达人)
│       ├── ws.py              #   WebSocket 处理 (实时通信桥梁)
│       └── push.py            #   WebSocket 推送 (消息推送员)

├── frontend/                 # Vue3 前端
│   ├── src/                   #   源代码
│   │   ├── views/             #     页面视图
│   │   │   ├── ChatView.vue   #       聊天页面
│   │   │   ├── DashboardView.vue  #   仪表盘
│   │   │   ├── TasksView.vue  #       任务管理
│   │   │   ├── AIInstancesView.vue  #  AI 实例
│   │   │   └── SettingsView.vue  #    设置
│   │   ├── stores/            #     状态管理
│   │   ├── api/               #     API 封装
│   │   ├── router.js          #     路由配置
│   │   ├── main.js            #     入口文件
│   │   └── App.vue            #     根组件
│   ├── package.json           #   依赖配置
│   ├── vite.config.js         #   Vite 配置
│   └── index.html             #   HTML 入口

├── config/                    # 配置 & 模板
│   ├── config.yaml            #   主配置 (总设置！)
│   ├── prompts/               #   Jinja2 提示词模板 (prompt 们～)
│   └── themes/                #   角色主题 (catgirl / programmer)

├── scripts/                   # 工具脚本
│   ├── preflight.sh           #   环境预检 (出发前检查！)
│   └── test_run.py            #   功能测试 (跑一跑试试看)

#   (其他配置文件)

└── data/                      # 运行时数据（gitignored）
    ├── .key                   #   加密密钥 (保密小密码)
    ├── chromadb/              #   向量数据库 (记忆仓库)
    ├── db/                    #   SQLite 数据库 (数据家)
    ├── logs/                  #   日志文件 (记录酱～)
    ├── outputs/               #   交付产物 (产出们！)
    ├── states/                #   任务快照 (存档点！)
    └── knowledge_base/        #   知识文件 (学习资料！)
```

---

## ❓ 常见问题 (来看看有没有你遇到的！)

**Q: 启动后 API 返回 502？**  
A: 确认 LLM 端点已启动并可访问喵～默认用 `http://localhost:11434`（Ollama）哦！

**Q: 如何更换 AI 模型？**  
A: 在 UI 的 Config Panel 中添加 AI Instance，或修改 `config/config.yaml` 的 `ai_pool.instances`就可以啦！

**Q: 任务卡死怎么办？**  
A: 可以在 UI 中撤销任务，或通过 API `POST /api/tasks/{id}/cancel` 取消后恢复哦！

**Q: 如何在 Windows 上运行？**  
A: 使用 `python main.py` 启动（会自动安装前端依赖并启动 Vue 前端），或者手动 `cd frontend && npm run dev` 就可以！

**Q: 如何调试 Agent 输出？**  
A: 设置 `system.log_level: DEBUG` 查看详细日志，或在 UI 的 Chat 页面查看 L2 层消息～

---

## 🎨 UI 设计 (新界面超好看！)

IReckon 前端采用 **毛玻璃 (Glassmorphism)** 设计风格，参考 [XinghuisamaBlogs](https://github.com/heiehiehi/XinghuisamaBlogs) 的视觉效果和 [AstrBot](https://astrbot.app) 的配色体系。

### 配色方案

```
主色        #3c96ca     品牌蓝
深蓝        #2b3f67     辅助色 (hover/强调)
紫色        #a855f7     渐变色 (与主蓝搭配)
背景基底    #f8fafc     亮色 / #0f172a 暗色
卡片背景    #f1f5f9     亮色 / #1e293b 暗色
文本主色    #0f172a     亮色 / #f1f5f9 暗色
成功        #28c840     状态绿色
警告        #febc2e     状态琥珀
错误        #ff5f57     状态红色
```

按钮渐变: `linear-gradient(135deg, #a855f7, #3c96ca)`

### 新 UI 组件

| 组件 | 文件 | 说明 |
|------|------|------|
| `SplashScreen` | `frontend/src/components/SplashScreen.vue` | 启动加载动画 — Logo 渐变环 + 进度条，仅首访显示 |
| `ClickEffect` | `frontend/src/components/ClickEffect.vue` | 点击涟漪 — Canvas 水波扩散反馈 |
| `BackgroundEffects` | `frontend/src/components/BackgroundEffects.vue` | 背景粒子 — 暗色萤火虫 / 亮色气泡 |
| `GlobalToolbox` | `frontend/src/components/GlobalToolbox.vue` | 浮动工具箱 — 右下角快捷操作 |
| `PageTransition` | `frontend/src/components/PageTransition.vue` | 页面切换 — fade+上滑过渡动画 |

### 视觉效果

- **毛玻璃卡片**: 所有面板统一 `backdrop-filter: blur(12px) saturate(180%)` + 半透明边框
- **动态渐变背景**: `linear-gradient(-45deg, #a18cd1, #fbc2eb, #a1c4fd, #c2e9fb)`，15s 循环动画
- **装饰性模糊球**: 固定背景层 `blur(100px+)` 的蓝紫半透明装饰圆
- **侧边栏**: 左侧固定 220px，玻璃质感，导航项带左侧发光指示条
- **字体**: Inter (UI) + Noto Serif SC (标题) + JetBrains Mono (代码)
- **滚动条**: 薄型，品牌蓝着色
- **启动画面**: 首次访问显示 SplashScreen，sessionStorage 控制只显示一次

### 局域网访问

启动后会自动检测并打印 LAN IP，同局域网设备可通过 `http://<LAN_IP>:3000` 访问。

---

## 📜 许可

MIT License — 详见项目 LICENSE 文件喵～ ✿

最后，谢谢使用 IReckon！希望它能帮你省掉超多麻烦！(๑•̀ᴗ-)✧ 一起加油吧！