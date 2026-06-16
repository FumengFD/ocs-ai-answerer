# OCS AI Answerer

## OCS 智能答题 API — 多模型支持版本

<div align="center">

[![GitHub Stars](https://img.shields.io/github/stars/FumengFD/ocs-ai-answerer?style=social)](https://github.com/FumengFD/ocs-ai-answerer/stargazers)
[![GitHub License](https://img.shields.io/github/license/FumengFD/ocs-ai-answerer)](https://github.com/FumengFD/ocs-ai-answerer/blob/main/LICENSE)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Waitress](https://img.shields.io/badge/Waitress-Production-00bb6d.svg)
![DeepSeek](https://img.shields.io/badge/DeepSeek-Flash%2FPro-orange.svg)
![Doubao](https://img.shields.io/badge/Doubao-1.6%20Thinking-purple.svg)

专为 [OCS 网课助手](https://docs.ocsjs.com/) 设计的智能答题 API，支持 DeepSeek、豆包等多个大语言模型。

</div>

---

## 与上游原版的差异

本项目基于 [lkd6666/ocs-ai-answerer](https://github.com/lkd6666/ocs-ai-answerer) v3.0，进行了以下增强：

| 类别 | 改动 |
|------|------|
| 模型 | `deepseek-chat` -> `deepseek-v4-flash`，`deepseek-reasoner` -> `deepseek-v4-pro`，豆包 -> `doubao-seed-1-6-thinking-250715` |
| 服务器 | Flask 开发服务器 -> **Waitress** 生产级 WSGI（4 线程） |
| 开箱即用 | 首次启动**自动从 `env.template` 创建 `.env`** |
| 前端 | 自动构建 Vue3 SPA；**无 Node.js 时回退静态 HTML** 界面 |
| 密钥 | 访问密钥**每次启动都显示**，不再丢失 |
| 题型 | 新增**连线题**支持（type=5，字母#分隔） |
| 优化 | 答案兜底、填空题智能检测、题目截断 |
| 配置 | config_panel 新增 **OCS 脚本配置**标签页（一键复制） |

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python ocs_ai_answerer_advanced.py
```

首次启动会自动创建 `.env` 配置文件。如需使用 AI 答题，编辑 `.env` 填入 API 密钥后重启。

### 3. 获取 API 密钥

- **DeepSeek**：https://platform.deepseek.com/api_keys -> 获取 `sk-xxx...`
- **豆包**：https://console.volcengine.com/ark -> 创建推理接入点

编辑 `.env`：

```env
MODEL_PROVIDER=auto

DEEPSEEK_API_KEY=sk-your-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com

DOUBAO_API_KEY=your-doubao-key
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
DOUBAO_MODEL=doubao-seed-1-6-thinking-250715
```

### 4. 配置 OCS 脚本

在 OCS 脚本的题库配置中导入 `ocs_config.json`，或手动设置答题 URL 为 `http://127.0.0.1:5000/api/answer`。

---

## 启动输出示例

```
+-----------------------------------------------------+
|      OCS智能答题API服务 - 多模型支持版本 v3.1        |
+-----------------------------------------------------+
|  静态 HTML: http://127.0.0.1:5000/                  |
|  数据可视化: http://127.0.0.1:5000/viewer           |
|  API文档: http://127.0.0.1:5000/docs                |
+-----------------------------------------------------+
|  接口地址: http://127.0.0.1:5000/api/answer         |
|  健康检查: http://127.0.0.1:5000/api/health         |
|  配置查询: http://127.0.0.1:5000/api/config         |
|  CSV数据: http://127.0.0.1:5000/api/csv             |
+-----------------------------------------------------+
|  当前模式: AUTO (智能选择)                           |
|  思考模式:  未启用                                   |
|  支持题型: 单选、多选、判断、填空、连线               |
+-----------------------------------------------------+
|  旧版HTML: http://127.0.0.1:5000/config_legacy      |
+-----------------------------------------------------+
```

---

## Web 界面

| 页面 | URL | 说明 |
|------|-----|------|
| 首页 | `/` | Vue3 SPA 或静态配置面板（自动选择） |
| 数据可视化 | `/viewer` | 答题记录图表和统计 |
| API 文档 | `/docs` | 在线 API 接口文档 |

> 内置 Node.js 时自动构建 Vue3 SPA，否则使用静态 HTML — 两种模式功能一致。

---

## API 接口

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/answer` | 否 | 答题接口（type: 0=单选 1=多选 3=填空 4=判断 5=连线） |
| GET | `/api/health` | 否 | 健康检查 |
| GET | `/api/config` | 是 | 查看配置 |
| POST | `/api/config` | 是 | 更新配置 |
| GET | `/api/csv` | 否 | 查看 CSV 数据 |
| DELETE | `/api/csv/clear` | 是 | 清空数据 |
| POST | `/api/auth/verify` | 否 | 验证访问密钥 |

认证方式：请求头 `X-API-Key: <访问密钥>` 或查询参数 `?key=<访问密钥>`。

---

## 配置参考

全部环境变量见 `env.template`。关键配置：

```env
# 模型提供商：deepseek / doubao / auto
MODEL_PROVIDER=auto

# 是否启用深度推理（全局）
ENABLE_REASONING=false
# 思考强度（仅豆包）：low / medium / high
REASONING_EFFORT=medium

# 多选题自动启用推理
AUTO_REASONING_FOR_MULTIPLE=true
# 图片题自动启用推理
AUTO_REASONING_FOR_IMAGES=true

# 温度 0.0~2.0（答题推荐 0.1）
TEMPERATURE=0.1
# 最大输出 token（普通模式）
MAX_TOKENS=500

# 服务端口
PORT=5000
```

---

## 常见问题

### 启动后浏览器打不开

确认使用 `http://127.0.0.1:5000` 而非 `http://0.0.0.0:5000`。

### 前端界面不显示

- 确保 `dist/` 或 `config_panel.html` 存在（仓库已包含）
- 刷新浏览器缓存

### 忘记访问密钥

```bash
# 查看密钥文件
cat .secret_key
# 或重新生成
rm .secret_key && python ocs_ai_answerer_advanced.py
```

### 缺少 API 密钥

编辑 `.env` 文件填入 `DEEPSEEK_API_KEY` 或 `DOUBAO_API_KEY`，重启服务。

---

## 部署

### 直接运行

```bash
pip install -r requirements.txt
python ocs_ai_answerer_advanced.py
```

已内置 Waitress 生产服务器，无需额外配置。

### systemd（Linux 开机自启）

```ini
[Unit]
Description=OCS AI Answerer
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/ocs-ai-answerer
ExecStart=python ocs_ai_answerer_advanced.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## FAQ (More)

<details>
<summary>展开更多问题</summary>

### 图片题目无法识别
1. 确认使用豆包模型：`MODEL_PROVIDER=doubao` 或 `auto`
2. 检查图片 URL 是否可访问
3. DeepSeek 不支持图片输入

### 如何提高准确率
- `AUTO_REASONING_FOR_MULTIPLE=true`（多选题自动推理）
- `AUTO_REASONING_FOR_IMAGES=true`（图片题自动推理）
- 降低温度：`TEMPERATURE=0.05`
- `MODEL_PROVIDER=auto` 智能选择最优模型

### API 密钥安全
- 使用 `.env` 文件存储密钥（已加入 `.gitignore`）
- 不要将真实密钥提交到 Git
- 使用访问密钥保护配置页面

</details>

---

## 更新日志

### v3.1 (2025-06)

- 模型更新：`deepseek-v4-flash` / `deepseek-v4-pro` / `doubao-seed-1-6-thinking-250715`
- Waitress 生产级 WSGI 替代 Flask 开发服务器
- 首次启动自动从 `env.template` 创建 `.env`
- 自动构建前端，无 Node.js 回退静态 HTML
- Windows CMD UTF-8 编码修复 + 边框对齐
- 启动地址改为 `127.0.0.1`
- 访问密钥每次启动显示
- `npm.cmd` 兼容性修复

### v3.0 (2025-11) — 上游

- Vue 3 + Element Plus 前端重构
- 访问密钥认证 + SHA256 + IP 限流
- 后端分页、数据可视化
- 保存并重启、智能轮询

---

## License

MIT License — 详见 [LICENSE](LICENSE)

---

<div align="center">

**基于** [lkd6666/ocs-ai-answerer](https://github.com/lkd6666/ocs-ai-answerer) v3.0

⭐ 如果这个项目对你有帮助，请给个 star！

</div>
