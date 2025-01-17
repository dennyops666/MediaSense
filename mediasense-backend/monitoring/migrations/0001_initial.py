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
            name="AlertRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="规则名称")),
                ("description", models.TextField(blank=True, verbose_name="规则描述")),
                (
                    "metric_type",
                    models.CharField(
                        choices=[
                            ("cpu", "CPU使用率"),
                            ("memory", "内存使用率"),
                            ("disk", "磁盘使用率"),
                            ("network", "网络流量"),
                            ("api_latency", "API响应时间"),
                            ("error_rate", "错误率"),
                            ("request_count", "请求数"),
                            ("task_count", "任务数"),
                        ],
                        max_length=20,
                        verbose_name="监控指标",
                    ),
                ),
                (
                    "operator",
                    models.CharField(
                        choices=[
                            ("gt", "大于"),
                            ("lt", "小于"),
                            ("gte", "大于等于"),
                            ("lte", "小于等于"),
                            ("eq", "等于"),
                            ("neq", "不等于"),
                        ],
                        max_length=10,
                        verbose_name="比较运算符",
                    ),
                ),
                ("threshold", models.FloatField(verbose_name="阈值")),
                (
                    "duration",
                    models.IntegerField(
                        default=5, help_text="指标超过阈值持续n分钟后触发告警", verbose_name="持续时间(分钟)"
                    ),
                ),
                (
                    "alert_level",
                    models.CharField(
                        choices=[("info", "信息"), ("warning", "警告"), ("critical", "严重")],
                        default="warning",
                        max_length=20,
                        verbose_name="告警级别",
                    ),
                ),
                ("is_active", models.IntegerField(default=1, verbose_name="是否启用")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="alert_rules",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建者",
                    ),
                ),
            ],
            options={
                "verbose_name": "告警规则",
                "verbose_name_plural": "告警规则",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="AlertHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "活动"), ("resolved", "已解决"), ("acknowledged", "已确认")],
                        default="active",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                ("metric_value", models.FloatField(verbose_name="指标值")),
                ("triggered_at", models.DateTimeField(auto_now_add=True, verbose_name="触发时间")),
                ("resolved_at", models.DateTimeField(blank=True, null=True, verbose_name="解决时间")),
                ("acknowledged_at", models.DateTimeField(blank=True, null=True, verbose_name="确认时间")),
                ("note", models.TextField(blank=True, verbose_name="备注")),
                (
                    "acknowledged_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="acknowledged_alerts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="确认者",
                    ),
                ),
                (
                    "rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alert_history",
                        to="monitoring.alertrule",
                        verbose_name="告警规则",
                    ),
                ),
            ],
            options={
                "verbose_name": "告警历史",
                "verbose_name_plural": "告警历史",
                "ordering": ["-triggered_at"],
            },
        ),
        migrations.CreateModel(
            name="Dashboard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="名称")),
                ("description", models.TextField(blank=True, verbose_name="描述")),
                (
                    "layout_type",
                    models.CharField(
                        choices=[("GRID", "网格布局"), ("FLOW", "流式布局")],
                        default="GRID",
                        max_length=20,
                        verbose_name="布局类型",
                    ),
                ),
                ("is_default", models.IntegerField(default=0, verbose_name="是否默认")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="创建者"
                    ),
                ),
            ],
            options={
                "verbose_name": "监控仪表板",
                "verbose_name_plural": "监控仪表板",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="DashboardWidget",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="名称")),
                (
                    "widget_type",
                    models.CharField(
                        choices=[
                            ("SYSTEM_OVERVIEW", "系统概览"),
                            ("PERFORMANCE_TREND", "性能趋势"),
                            ("ALERT_STATISTICS", "告警统计"),
                            ("CUSTOM_METRICS", "自定义指标"),
                        ],
                        max_length=20,
                        verbose_name="组件类型",
                    ),
                ),
                ("config", models.JSONField(default=dict, verbose_name="配置")),
                ("position", models.JSONField(default=dict, verbose_name="位置")),
                ("is_visible", models.IntegerField(default=1, verbose_name="是否可见")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "dashboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="widgets",
                        to="monitoring.dashboard",
                        verbose_name="所属仪表板",
                    ),
                ),
            ],
            options={
                "verbose_name": "仪表板组件",
                "verbose_name_plural": "仪表板组件",
                "ordering": ["dashboard", "created_at"],
            },
        ),
        migrations.CreateModel(
            name="MonitoringVisualization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="图表名称")),
                ("description", models.TextField(blank=True, verbose_name="图表描述")),
                (
                    "chart_type",
                    models.CharField(
                        choices=[("line", "折线图"), ("bar", "柱状图"), ("gauge", "仪表盘"), ("pie", "饼图")],
                        default="line",
                        max_length=20,
                        verbose_name="图表类型",
                    ),
                ),
                (
                    "metric_type",
                    models.CharField(
                        choices=[
                            ("cpu", "CPU使用率"),
                            ("memory", "内存使用率"),
                            ("disk", "磁盘使用率"),
                            ("network", "网络流量"),
                            ("api_latency", "API响应时间"),
                            ("error_rate", "错误率"),
                            ("request_count", "请求数"),
                            ("task_count", "任务数"),
                        ],
                        max_length=20,
                        verbose_name="指标类型",
                    ),
                ),
                (
                    "time_range",
                    models.IntegerField(default=60, help_text="统计最近n分钟的数据", verbose_name="时间范围(分钟)"),
                ),
                (
                    "interval",
                    models.IntegerField(default=60, help_text="数据聚合的时间间隔", verbose_name="统计间隔(秒)"),
                ),
                (
                    "aggregation_method",
                    models.CharField(
                        choices=[
                            ("avg", "平均值"),
                            ("max", "最大值"),
                            ("min", "最小值"),
                            ("sum", "求和"),
                            ("count", "计数"),
                        ],
                        default="avg",
                        max_length=20,
                        verbose_name="聚合方法",
                    ),
                ),
                (
                    "warning_threshold",
                    models.FloatField(blank=True, help_text="超过此值显示警告", null=True, verbose_name="警告阈值"),
                ),
                (
                    "critical_threshold",
                    models.FloatField(blank=True, help_text="超过此值显示严重警告", null=True, verbose_name="严重阈值"),
                ),
                ("is_active", models.IntegerField(default=1, verbose_name="是否启用")),
                (
                    "refresh_interval",
                    models.IntegerField(default=30, help_text="数据自动刷新的间隔", verbose_name="刷新间隔(秒)"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("last_generated", models.DateTimeField(blank=True, null=True, verbose_name="上次生成时间")),
                (
                    "cached_data",
                    models.JSONField(blank=True, help_text="缓存的图表数据", null=True, verbose_name="缓存数据"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="monitoring_visualizations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="创建者",
                    ),
                ),
            ],
            options={
                "verbose_name": "监控可视化",
                "verbose_name_plural": "监控可视化",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="SystemMetrics",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "metric_type",
                    models.CharField(
                        choices=[
                            ("cpu", "CPU使用率"),
                            ("memory", "内存使用率"),
                            ("disk", "磁盘使用率"),
                            ("network", "网络流量"),
                            ("api_latency", "API响应时间"),
                            ("error_rate", "错误率"),
                            ("request_count", "请求数"),
                            ("task_count", "任务数"),
                        ],
                        max_length=20,
                        verbose_name="指标类型",
                    ),
                ),
                ("value", models.FloatField(verbose_name="指标值")),
                ("timestamp", models.DateTimeField(auto_now_add=True, verbose_name="记录时间")),
                ("metadata", models.JSONField(blank=True, default=dict, verbose_name="元数据")),
            ],
            options={
                "verbose_name": "系统指标",
                "verbose_name_plural": "系统指标",
                "ordering": ["-timestamp"],
                "indexes": [models.Index(fields=["metric_type", "-timestamp"], name="monitoring__metric__5bdd21_idx")],
            },
        ),
        migrations.CreateModel(
            name="AlertNotificationConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("email", "邮件"),
                            ("sms", "短信"),
                            ("webhook", "Webhook"),
                            ("dingtalk", "钉钉"),
                            ("wechat", "企业微信"),
                        ],
                        max_length=20,
                        verbose_name="通知类型",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="配置名称")),
                ("config", models.JSONField(help_text="不同通知类型的具体配置参数", verbose_name="配置详情")),
                (
                    "alert_levels",
                    models.JSONField(default=list, help_text="接收哪些级别的告警", verbose_name="接收的告警级别"),
                ),
                ("is_active", models.IntegerField(default=1, verbose_name="是否启用")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alert_notification_configs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "告警通知配置",
                "verbose_name_plural": "告警通知配置",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["user", "notification_type"], name="monitoring__user_id_f5e0a3_idx"),
                    models.Index(fields=["created_at"], name="monitoring__created_2bf7cd_idx"),
                ],
            },
        ),
        migrations.AddIndex(
            model_name="alertrule",
            index=models.Index(fields=["metric_type", "is_active"], name="monitoring__metric__1349ba_idx"),
        ),
        migrations.AddIndex(
            model_name="alertrule",
            index=models.Index(fields=["created_at"], name="monitoring__created_e57411_idx"),
        ),
        migrations.AddIndex(
            model_name="alerthistory",
            index=models.Index(fields=["rule", "status"], name="monitoring__rule_id_0ac316_idx"),
        ),
        migrations.AddIndex(
            model_name="alerthistory",
            index=models.Index(fields=["triggered_at"], name="monitoring__trigger_ba7964_idx"),
        ),
        migrations.AddIndex(
            model_name="dashboard",
            index=models.Index(fields=["created_by", "-created_at"], name="monitoring__created_d86c59_idx"),
        ),
        migrations.AddIndex(
            model_name="dashboardwidget",
            index=models.Index(fields=["dashboard", "widget_type"], name="monitoring__dashboa_6f7e96_idx"),
        ),
        migrations.AddIndex(
            model_name="monitoringvisualization",
            index=models.Index(fields=["metric_type", "is_active"], name="monitoring__metric__3cd24a_idx"),
        ),
        migrations.AddIndex(
            model_name="monitoringvisualization",
            index=models.Index(fields=["created_at"], name="monitoring__created_b135c4_idx"),
        ),
    ]
