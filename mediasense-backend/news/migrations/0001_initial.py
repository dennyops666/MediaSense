# Generated by Django 5.1.4 on 2025-01-13 04:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="分类名称")),
                ("description", models.TextField(blank=True, verbose_name="分类描述")),
                ("level", models.IntegerField(default=1, verbose_name="分类层级")),
                ("sort_order", models.IntegerField(default=0, verbose_name="排序")),
                ("is_active", models.IntegerField(default=1, verbose_name="是否启用")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="news.newscategory",
                        verbose_name="父分类",
                    ),
                ),
            ],
            options={
                "verbose_name": "新闻分类",
                "verbose_name_plural": "新闻分类",
                "db_table": "news_category",
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="NewsArticle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="标题")),
                ("content", models.TextField(verbose_name="正文内容")),
                ("summary", models.TextField(blank=True, verbose_name="摘要")),
                ("source", models.CharField(blank=True, max_length=100, verbose_name="来源")),
                ("author", models.CharField(blank=True, max_length=100, verbose_name="作者")),
                ("url", models.CharField(max_length=500, unique=True, verbose_name="原文链接")),
                ("tags", models.JSONField(default=list, verbose_name="标签")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "草稿"),
                            ("pending", "待审核"),
                            ("published", "已发布"),
                            ("rejected", "已拒绝"),
                            ("archived", "已归档"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                ("sentiment_score", models.FloatField(default=0.0, verbose_name="情感得分")),
                ("publish_time", models.DateTimeField(blank=True, null=True, verbose_name="发布时间")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("read_count", models.PositiveIntegerField(default=0, verbose_name="阅读数")),
                ("like_count", models.PositiveIntegerField(default=0, verbose_name="点赞数")),
                ("comment_count", models.PositiveIntegerField(default=0, verbose_name="评论数")),
                ("review_time", models.DateTimeField(blank=True, null=True, verbose_name="审核时间")),
                ("review_comment", models.TextField(blank=True, verbose_name="审核意见")),
                (
                    "reviewer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_articles",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="审核人",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="articles",
                        to="news.newscategory",
                        verbose_name="所属分类",
                    ),
                ),
            ],
            options={
                "verbose_name": "新闻文章",
                "verbose_name_plural": "新闻文章",
                "db_table": "news_article",
                "ordering": ["-publish_time", "-id"],
            },
        ),
        migrations.CreateModel(
            name="NewsAuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("submit", "提交审核"),
                            ("assign", "分配审核"),
                            ("approve", "审核通过"),
                            ("reject", "审核拒绝"),
                            ("withdraw", "撤回审核"),
                        ],
                        max_length=20,
                        verbose_name="审核动作",
                    ),
                ),
                (
                    "from_status",
                    models.CharField(
                        choices=[
                            ("draft", "草稿"),
                            ("pending", "待审核"),
                            ("published", "已发布"),
                            ("rejected", "已拒绝"),
                            ("archived", "已归档"),
                        ],
                        max_length=20,
                        verbose_name="原状态",
                    ),
                ),
                (
                    "to_status",
                    models.CharField(
                        choices=[
                            ("draft", "草稿"),
                            ("pending", "待审核"),
                            ("published", "已发布"),
                            ("rejected", "已拒绝"),
                            ("archived", "已归档"),
                        ],
                        max_length=20,
                        verbose_name="新状态",
                    ),
                ),
                ("comment", models.TextField(blank=True, verbose_name="审核意见")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audit_logs",
                        to="news.newsarticle",
                        verbose_name="新闻文章",
                    ),
                ),
                (
                    "operator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="audit_operations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="操作人",
                    ),
                ),
            ],
            options={
                "verbose_name": "审核日志",
                "verbose_name_plural": "审核日志",
                "db_table": "news_audit_log",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["article", "action"], name="news_audit__article_97259d_idx"),
                    models.Index(fields=["operator", "created_at"], name="news_audit__operato_e8dd4a_idx"),
                ],
            },
        ),
        migrations.AddIndex(
            model_name="newscategory",
            index=models.Index(fields=["parent_id"], name="news_catego_parent__52eccc_idx"),
        ),
        migrations.AddIndex(
            model_name="newscategory",
            index=models.Index(fields=["level"], name="news_catego_level_d786c5_idx"),
        ),
        migrations.AddIndex(
            model_name="newscategory",
            index=models.Index(fields=["is_active"], name="news_catego_is_acti_4de217_idx"),
        ),
        migrations.AddIndex(
            model_name="newsarticle",
            index=models.Index(fields=["status"], name="news_articl_status_a95c4c_idx"),
        ),
        migrations.AddIndex(
            model_name="newsarticle",
            index=models.Index(fields=["category"], name="news_articl_categor_ac462d_idx"),
        ),
        migrations.AddIndex(
            model_name="newsarticle",
            index=models.Index(fields=["publish_time"], name="news_articl_publish_50495a_idx"),
        ),
        migrations.AddIndex(
            model_name="newsarticle",
            index=models.Index(fields=["created_at"], name="news_articl_created_4ed0e6_idx"),
        ),
        migrations.AddIndex(
            model_name="newsarticle",
            index=models.Index(fields=["read_count"], name="news_articl_read_co_12fbd9_idx"),
        ),
        migrations.AddIndex(
            model_name="newsarticle",
            index=models.Index(fields=["like_count"], name="news_articl_like_co_a46174_idx"),
        ),
        migrations.AddIndex(
            model_name="newsarticle",
            index=models.Index(fields=["comment_count"], name="news_articl_comment_401d7a_idx"),
        ),
    ]
