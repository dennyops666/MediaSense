-- 创建数据库
CREATE DATABASE IF NOT EXISTS mediasense
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