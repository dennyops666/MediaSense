以下是整合了先前所有需求、包含「数据库逻辑结构设计」「建表脚本」「GPT-4.0+ 接口调用方案」「前后端实现思路」「运行环境部署方法」等内容的**完整开发文档**。此文档旨在帮助团队在 **Python + Django + Vue + MySQL + GPT-4.0+** 技术栈下，从零开始搭建并部署一套简易舆情监控/新闻聚合系统。

---

# 1. 前言

## 1.1 编写目的

本开发文档面向整个项目团队（后端开发、前端开发、测试人员、运维人员以及项目管理层），力求：

1. 对系统需求和整体架构做出完整说明，保证成员对各模块的功能和交互有共同认知。  
2. 提供数据库逻辑结构设计与建表脚本，便于团队快速初始化并理解数据层关系。  
3. 说明如何在后端（Django）结合 GPT-4.0+ 完成高阶文本分析（情感、摘要、关键词提炼等）。  
4. 指导前端（Vue）实现新闻聚合与可视化展示（ECharts），并说明权限管理、API 交互细节。  
5. 给出运行环境部署方法，确保团队可在 Linux 服务器上顺利安装依赖、部署应用并上线运行。  

本项目的核心目标是**多渠道数据采集 + AI 驱动的舆情监控与新闻聚合 + 可视化展示**。如后续需扩展更多功能或大规模分发，也能基于本文档进行增补或改造。

## 1.2 文档结构概述

- **第 2 章：开发环境与主要依赖**  
- **第 3 章：系统整体架构**  
- **第 4 章：数据库设计**（包含逻辑结构与建表脚本）  
- **第 5 章：爬虫与数据采集**  
- **第 6 章：NLP 与 GPT-4.0+ AI 接口**  
- **第 7 章：Django 后端业务逻辑与接口**  
- **第 8 章：Vue 前端实现及可视化**  
- **第 9 章：部署与运行环境准备**（详细的部署方法）  
- **第 10 章：测试与质量保证**  
- **第 11 章：项目进度安排与里程碑**  
- **第 12 章：后续扩展与性能优化**  
- **第 13 章：附录（术语表、工具资源等）**

---

# 2. 开发环境与主要依赖

## 2.1 软件与硬件环境

- **操作系统**：Linux (Ubuntu 20.04+ / CentOS 7+)；本地开发可使用 Windows/macOS/Linux  
- **硬件**：2~4 核 CPU，≥8 GB 内存，≥50 GB 磁盘空间  
- **网络**：需可访问外网，以拉取依赖包、抓取新闻站点与调用 OpenAI API

## 2.2 主要技术栈

1. **后端**：  
   - Python 3.8+  
   - Django 3/4 及可选 Django REST Framework  
2. **前端**：  
   - Vue.js (2.x/3.x)  
   - Axios (接口请求)  
   - ECharts (可视化图表)  
3. **数据库**：  
   - MySQL 5.7+（InnoDB 引擎）  
4. **AI 服务**：  
   - OpenAI GPT-4.0+，用于情感分析、关键点提取、摘要等

## 2.3 依赖示例

- **Python**：requests, openai, django, djangorestframework, mysqlclient, jieba(可选)  
- **Node**：vue, vue-router, vuex/pinia, axios, echarts, element-ui/antd-vue(可选)

---

# 3. 系统整体架构

## 3.1 功能目标

1. **多渠道数据采集**：爬虫周期性抓取新闻（门户网站、RSS、社交媒体等）  
2. **AI 分析**：将文本送往 GPT-4.0+ 进行深度情感、关键词或摘要处理  
3. **新闻聚合与可视化**：Django 后端提供数据 API，前端 Vue 显示聚合列表与可视化图表  
4. **用户权限**：管理员可配置爬虫、查看 AI 日志，普通用户仅查看新闻  
5. **运行部署**：在单台 Linux 服务器上完成后端、前端与数据库部署

## 3.2 模块与交互示意

1. **采集模块（爬虫）**：读取爬虫配置 → 抓取内容 → 写入 MySQL  
2. **AI 模块（GPT-4.0+）**：对新抓取文本或指定新闻进行情感/摘要 → 回写到数据库  
3. **后端（Django）**：聚合 news_table 数据 → 提供 RESTful API  
4. **前端（Vue）**：用户请求 API → Axios 返回数据 → ECharts 绘制图表

---

# 4. 数据库设计

## 4.1 建表脚本 (MySQL)

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS news_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE news_db;

-- 用户表 user_info
CREATE TABLE IF NOT EXISTS user_info (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    email VARCHAR(100),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 新闻/舆情主表 news_table
CREATE TABLE IF NOT EXISTS news_table (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) DEFAULT '',
    publish_time DATETIME,
    content LONGTEXT,
    sentiment VARCHAR(10) DEFAULT NULL,
    keywords VARCHAR(500) DEFAULT NULL,
    source VARCHAR(50) DEFAULT '',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 爬虫配置表 crawler_config
CREATE TABLE IF NOT EXISTS crawler_config (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    site_name VARCHAR(50) NOT NULL,
    url VARCHAR(255) NOT NULL,
    frequency VARCHAR(20) DEFAULT 'daily',
    use_proxy TINYINT(1) DEFAULT 0,
    is_enabled TINYINT(1) DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- AI 分析日志表 analysis_log
CREATE TABLE IF NOT EXISTS analysis_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    news_id BIGINT NOT NULL,
    analysis_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    model_used VARCHAR(50) DEFAULT 'gpt-4',
    tokens_consumed INT DEFAULT 0,
    analysis_result TEXT,
    CONSTRAINT fk_analysis_news
      FOREIGN KEY (news_id) REFERENCES news_table(id)
      ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

COMMIT;
```

## 4.2 数据库逻辑结构

1. **user_info**  
   - 存储登录账号信息：`username`, `password`(哈希), `role`(admin/user/guest)  
   - 与其他表无外键关系，但在业务逻辑中控制权限  
2. **news_table**  
   - 核心新闻存储：`title`, `content`, `publish_time`, `sentiment`, `keywords` 等  
   - 爬虫写入后，AI 分析结果也可更新此表中的 `sentiment`, `keywords`  
3. **crawler_config**  
   - 记录爬虫抓取站点、频率等，由管理员在后端管理  
4. **analysis_log**  
   - 外键 `news_id` 指向 `news_table(id)`，记录 GPT-4.0+ 调用详情  
   - 多次分析可产生多条记录

在逻辑上，**news_table** 与 **analysis_log** 为一对多关系；**crawler_config** 供爬虫脚本参考；**user_info** 用于系统身份验证和权限区分。

---

# 5. 爬虫与数据采集

## 5.1 框架与调度

- **Requests + BeautifulSoup**：轻量级 HTML 解析；对 JS 动态站点可视需求使用 Selenium/pyppeteer  
- **调度**：可使用 Linux cron 或 Django management command (APS cheduler)

## 5.2 防爬策略应对

- **代理池**：在 `crawler_config` 中 `use_proxy=1` 即启用代理  
- **限速**：随机 sleep，模拟人工访问  
- **RSS 优先**：能减少对 DOM 的复杂解析，也减少防爬风险

## 5.3 数据提取 & 去重

- 解析 HTML 提取 `title`, `content`, `publish_time` …  
- 简要做哈希或相似度对比，避免重复  
- 最终将有效数据插入 `news_table`

---

# 6. NLP 与 GPT-4.0+ AI 接口

## 6.1 本地 NLP（可选）

- **jieba**：分词或关键词统计  
- 对不太复杂的文本可做简单情感分析，但精准度有限

## 6.2 GPT-4.0+ 调用

1. **API Key 配置**：在后端 `.env` 里添加 `OPENAI_API_KEY=sk-xxxxxx`  
2. **示例**（Python）：
   ```python
   import openai
   import os

   openai.api_key = os.getenv("OPENAI_API_KEY")

   def analyze_text_gpt4(text):
       response = openai.ChatCompletion.create(
           model="gpt-4",
           messages=[
               {"role":"system","content":"你是一个舆情分析助手。"},
               {"role":"user","content":f"请对以下文本进行分析:{text}"}
           ],
           temperature=0.2
       )
       return response
   ```
3. **写入数据库**：  
   - 解析得到 `sentiment`, `keywords` → 更新 `news_table`  
   - 记录在 `analysis_log`（包含 `tokens_consumed`, `analysis_result` 等）

## 6.3 速率限制 & 异常

- GPT-4.0+ 并发 & tokens/分钟限制更严格  
- 需在后端排队处理或拆分长文本  
- 遇到 429/503 需重试并记录日志

---

# 7. Django 后端业务逻辑与接口

## 7.1 模块划分

1. **User/权限**：可使用 `django.contrib.auth` 或自定义 `user_info` 同步  
2. **News/舆情**：对 `news_table` 提供增删改查 & AI 分析触发  
3. **Admin 后台**：管理 `crawler_config`、查看 `analysis_log`、操作用户角色

## 7.2 接口定义（示例）

- **GET** `/api/news/list`  
  - 参数：`keyword`, `startTime`, `endTime`, `sentiment`  
  - 返回：`{ code:0, data:[...] }`
- **POST** `/api/admin/crawler`  
  - Body: `{"site_name":"xx","url":"...","frequency":"daily","use_proxy":true}`
- **POST** `/api/analysis/gpt4`  
  - 指定 `news_id`  
  - 后端调用 GPT-4.0+ 并写数据库

## 7.3 安全与权限

- **Django REST Framework**：可选 `TokenAuth` 或 `JWTAuth`  
- **role**：admin 可以做更多操作，user/guest 仅能查询  
- **敏感信息**：OPENAI_API_KEY 不下发给前端

---

# 8. Vue 前端实现及可视化

## 8.1 项目结构

```text
src/
  ├─ api/         # axios调用后端
  ├─ components/  # 复用组件
  ├─ views/       # 页面级组件
  ├─ router/
  ├─ store/       # vuex/pinia
  └─ App.vue
```

## 8.2 主要页面

1. **登录注册**：请求后端 `/api/auth/...`  
2. **新闻列表**：输入检索条件 → Vue 调用 `/api/news/list` → 渲染列表  
3. **舆情可视化**：ECharts 饼图/折线/词云  
4. **管理页面**：管理爬虫配置、日志查看（仅 admin）

## 8.3 ECharts 细节

- **折线图**：时间段内新闻数或情感数量  
- **饼图**：pos/neg/neu 占比  
- **词云**：keywords 及其出现频次

---

# 9. 部署与运行环境准备

## 9.1 环境要求

- **Linux**: Ubuntu 20.04/CentOS 7  
- **Python** 3.8+  
- **Node.js** 16+  
- **MySQL** 5.7+  
- **Nginx** (可选) 用于反向代理 & 前端静态资源

## 9.2 安装流程

### 9.2.1 MySQL 初始化

```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation

# 登录后执行建表脚本:
mysql -u root -p < news_db.sql
```

### 9.2.2 部署 Django 后端

1. **拉取代码**  
   ```bash
   git clone https://github.com/.../news-backend.git
   cd news-backend
   ```
2. **创建虚拟环境并安装依赖**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **配置 .env**  
   ```bash
   DEBUG=False
   SECRET_KEY=xxxx
   DATABASE_URL=mysql://root:password@127.0.0.1:3306/news_db
   OPENAI_API_KEY=sk-xxxxxx
   GPT_MODEL=gpt-4
   ```
4. **迁移与测试**  
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   # 浏览器访问 http://<server-ip>:8000/
   ```
5. **生产模式 (Gunicorn + Nginx)**  
   ```bash
   pip install gunicorn
   gunicorn news_backend.wsgi:application --bind 0.0.0.0:8000
   ```
   - Nginx 反向代理到 `localhost:8000`

### 9.2.3 部署 Vue 前端

1. **拉取前端代码**  
   ```bash
   git clone https://github.com/.../news-frontend.git
   cd news-frontend
   npm install
   ```
2. **构建打包**  
   ```bash
   npm run build
   # 生成 dist/
   ```
3. **Nginx 配置**（示例）
   ```nginx
   server {
     listen 80;
     server_name <server-ip-or-domain>;

     location / {
       root /opt/news-frontend/dist;
       try_files $uri $uri/ /index.html;
     }

     location /api/ {
       proxy_pass http://127.0.0.1:8000/;
     }
   }
   ```
   - `sudo nginx -t && sudo systemctl restart nginx`

### 9.2.4 定时爬虫

- **cron** 或 **systemd**：
  ```bash
  crontab -e
  # 每小时执行
  0 * * * * /opt/news-backend/venv/bin/python /opt/news-backend/manage.py crawl_sites
  ```

### 9.2.5 验证

- **后端 API**：`curl http://localhost:8000/api/news/list` 是否返回 JSON  
- **前端页面**：浏览 `http://<server-ip>/` 是否可访问前端并正常请求 `/api/`  
- **AI 调用**：对某条新闻发起 GPT-4.0+ 分析，查看 `analysis_log` 是否记录

---

# 10. 测试与质量保证

## 10.1 测试范围

- **功能性**：爬虫抓取、AI 分析写入、新闻检索、前端可视化  
- **性能**：并发访问下的响应速度、OpenAI tokens 费用监控  
- **安全**：角色越权、SQL 注入、API Key 泄漏等

## 10.2 测试用例

- 管理员新增爬虫目标 → 每小时后查看 `news_table`  
- AI 分析多条新闻 → 统计 `analysis_log` 记录  
- 并发 50+ 用户访问可视化页面 → 观察响应时间

## 10.3 缺陷管理与修复

- 采用 GitHub Issues / Jira 记录并分配修复  
- 回归测试 → Merge 主分支

---

# 11. 项目进度安排与里程碑

## 11.1 开发阶段

1. 环境搭建 & 数据库设计：1~2 周  
2. 爬虫 + AI 对接：2~3 周  
3. 后端 API + 前端页面：2 周  
4. 联调测试 & 优化：1~2 周  
5. 部署上线：1 周

## 11.2 关键里程碑

- **M1**：数据库结构 & Django 搭建完毕  
- **M2**：爬虫可抓取、GPT-4.0+ 测试通过  
- **M3**：前端完成主要页面，后端 API 对接成功  
- **M4**：功能联调、测试收尾  
- **M5**：正式上线

## 11.3 风险管理

- **OpenAI 调用费用**：需限流或预先截断文本  
- **防爬难度**：若站点更改结构或升级封锁  
- **数据库扩展**：若数据量激增，需分表或分布式

---

# 12. 后续扩展与性能优化

## 12.1 新功能展望

- 短视频评论或社交平台深度爬虫  
- 更复杂的话题聚类、自动预警  
- 多语言支持

## 12.2 性能提升

- 分布式爬虫、Redis 缓存热点搜索  
- 负载均衡：多台 Django 部署  
- 监控：Prometheus + Grafana

## 12.3 版本规划

- **v1.0**：核心功能落地 + GPT-4.0+  
- **v2.0**：分布式、多维可视化  
- **v3.0**：更高级 AI 推理、实时预警

---

# 13. 附录

## 13.1 术语表

- **GPT-4.0+**：OpenAI 高阶语言模型  
- **analysis_log**：记录 AI 分析 tokens 数量、结果 JSON  
- **crawler_config**：站点抓取配置  
- **sentiment**：正负面情感或中性标签

## 13.2 相关工具与资源

- **MySQL Workbench**：数据库可视化管理  
- **Docker / Docker Compose**：容器化部署可选  
- **Element UI / Ant Design Vue**：可加速前端后台页面开发  
- **Postman / Insomnia**：接口测试

---

## 结语

本开发文档覆盖了**需求到实现**的方方面面：**数据库逻辑结构设计**、**GPT-4.0+ 接口集成**、**爬虫实现要点**、**前后端交互**以及**Linux 服务器上的部署方法**等。项目组可据此在最短时间内搭建并上线「简易舆情监控/新闻聚合系统」，并在后期视业务与技术需求进行功能扩展或大规模分布式演进。愿项目开发顺利并为舆情分析与新闻聚合带来实际价值！