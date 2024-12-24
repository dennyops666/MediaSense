以下是**更加易于 AI 解析**的版本，将原有的开发文档内容用更**结构化、条列化**的方式呈现，以便各类 AI 模型或自动处理程序快速提取信息。虽然整体逻辑未变，但段落和语句尽量更短、更直观。

---

## 1. 前言

- **文档目的**: 指导在「Python + Django + Vue + MySQL + GPT-4.0+」技术栈下实现并部署“简易舆情监控/新闻聚合系统”。  
- **主要内容**:  
  1. 数据库设计（包含逻辑结构与建表脚本）  
  2. 爬虫 & AI 集成要点（GPT-4.0+）  
  3. Django 后端 & Vue 前端实现  
  4. Linux 服务器环境部署方法  

---

## 2. 开发环境与主要依赖

1. **操作系统**: Linux (Ubuntu/CentOS)  
2. **硬件**: CPU 2~4 核、≥8 GB 内存、≥50 GB 磁盘  
3. **后端**:  
   - Python 3.8+  
   - Django 3/4 (可含 Django REST Framework)  
   - OpenAI Python SDK (GPT-4.0+)  
4. **前端**:  
   - Vue.js (2/3)  
   - Axios、ECharts  
5. **数据库**: MySQL 5.7+ (InnoDB)

---

## 3. 系统整体架构

- **采集层（爬虫）**: Requests + BeautifulSoup + 代理/定时任务  
- **AI 分析（GPT-4.0+）**: 深度情感、关键词、摘要  
- **后端（Django）**: 数据库操作 + RESTful API + 后台管理  
- **前端（Vue）**: Axios 调用后端，ECharts 可视化  
- **数据库（MySQL）**: 存储用户、新闻、爬虫配置、AI 分析日志

---

## 4. 数据库设计

### 4.1 建表脚本 (MySQL)

```sql
CREATE DATABASE IF NOT EXISTS news_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE news_db;

CREATE TABLE IF NOT EXISTS user_info (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    email VARCHAR(100),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

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
);

CREATE TABLE IF NOT EXISTS crawler_config (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    site_name VARCHAR(50) NOT NULL,
    url VARCHAR(255) NOT NULL,
    frequency VARCHAR(20) DEFAULT 'daily',
    use_proxy TINYINT(1) DEFAULT 0,
    is_enabled TINYINT(1) DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

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
);

COMMIT;
```

### 4.2 逻辑结构

- **user_info**: 登录账号，`role` 管理权限  
- **news_table**: 存储新闻正文 & AI 分析结果 (`sentiment`, `keywords`)  
- **crawler_config**: 爬虫目标配置  
- **analysis_log**: 多次 AI 分析记录 (`news_id` 外键 → `news_table`)

---

## 5. 爬虫与数据采集

1. **框架**: Requests + BeautifulSoup  
2. **调度**: cron / Django management command  
3. **防爬策略**: 代理池、限速、RSS 优先  
4. **存储**: 数据写入 `news_table`，重复检查 (title + 内容哈希)

---

## 6. NLP 与 GPT-4.0+ 接口

1. **本地 NLP** (可选): jieba 分词  
2. **GPT-4.0+**:  
   - 在后端 `.env` 配置 `OPENAI_API_KEY`  
   - 调用 `openai.ChatCompletion.create(model="gpt-4", ...)`  
   - 将返回的情感/关键词/摘要写 `news_table` + 记录 `analysis_log`  
3. **异常/限流**: GPT-4.0+ 有并发 & token 限制，需限流或分批

---

## 7. Django 后端业务逻辑与接口

1. **User/权限**: 登录、注册、角色 (admin/user/guest)  
2. **News**: `/api/news/list`、`/api/news/detail/<id>`、可选 `/api/analysis/gpt4`  
3. **Admin**: `/api/admin/crawler` (增删改抓取规则)、查看 AI 分析日志  
4. **安全**: Token/JWT 认证，隐藏 `OPENAI_API_KEY`

---

## 8. Vue 前端实现及可视化

1. **目录结构**: `src/api/`, `src/views/`, `src/components/`, `router/`, `store/`  
2. **主要页面**:  
   - 登录 / 注册  
   - 新闻列表 (keyword + 时间筛选)  
   - 舆情可视化 (ECharts：饼图/折线/词云)  
   - 后台管理 (爬虫配置 / AI 日志)  
3. **ECharts 细节**:  
   - 折线：时间趋势  
   - 饼图：情感占比  
   - 词云：keywords 频次

---

## 9. 部署与运行环境准备

### 9.1 环境要求

- Linux: Ubuntu/CentOS  
- Python3, Node.js, MySQL, Nginx/Gunicorn

### 9.2 安装流程

1. **安装 MySQL**, 执行脚本 `news_db.sql`  
2. **部署 Django**:  
   - `git clone` → `python3 -m venv venv` → `pip install -r requirements.txt`  
   - `.env` 配置: `DATABASE_URL`, `OPENAI_API_KEY` 等  
   - `python manage.py migrate` → `python manage.py runserver` 测试  
   - 生产可用 `gunicorn + Nginx`  
3. **部署 Vue**:  
   - `npm install` → `npm run build`  
   - Nginx 静态托管 `dist/`，`location /api` 反向代理到 Django  
4. **定时爬虫**:  
   - cron: `0 * * * * /path/to/python manage.py crawl_sites`

---

## 10. 测试与质量保证

1. **功能测试**: 爬虫数据入库、AI 分析日志写入、前端可视化  
2. **性能测试**: 并发访问、OpenAI tokens 费用监控  
3. **安全测试**: 验证角色权限、API 注入、防爬

---

## 11. 项目进度与里程碑

1. **阶段1**: DB 设计 & Django 搭建 (1-2 周)  
2. **阶段2**: 爬虫 + GPT4 集成 (2-3 周)  
3. **阶段3**: 后端 API & 前端页面 (2 周)  
4. **阶段4**: 测试 & 优化 (1-2 周)  
5. **阶段5**: 部署 & 验收 (1 周)

---

## 12. 后续扩展与性能优化

1. **更多数据源**: 微博、短视频平台  
2. **分布式爬虫**: 多节点并行  
3. **缓存**: Redis 热点搜索  
4. **大规模**: 负载均衡、多台 Django

---

## 13. 附录

### 13.1 术语表

- **GPT-4.0+**: OpenAI 最新高阶模型  
- **analysis_log**: 记录 AI 分析 tokens、返回结果  
- **crawler_config**: 爬虫站点配置  
- **sentiment**: 正负中立情感标签

### 13.2 工具与资源

- **MySQL Workbench**: DB 可视化管理  
- **Docker**: 可选容器化  
- **Prometheus/Grafana**: 性能监控  
- **Element UI**: Vue 组件库  

---

**说明**: 以上结构化文档更便于 AI 或自动化工具解析其要点（数据库字段、接口流程、部署步骤、技术栈等）。各章节可根据项目规模或团队情况灵活增删。祝项目开发和部署成功！