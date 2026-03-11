"""
业务定时任务示例

包含一些实际业务场景中常用的定时任务
"""
from datetime import datetime
from loguru import logger
from celery_tasks.celery_app import app as celery_app


@celery_app.task(name="celery_tasks.beats.business.send_daily_report")
def send_daily_report():
    """
    发送每日报告

    模拟每天下午 6 点发送日报的任务
    """
    logger.info("[定时任务] 开始生成并发送每日报告")

    # 模拟数据收集
    report_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_users": 1000,
        "new_users": 50,
        "active_users": 800,
        "orders": 120,
    }

    # 模拟发送邮件或通知
    logger.info(f"报告数据：{report_data}")
    logger.success("[定时任务] 每日报告发送成功")

    return {"status": "success", "report_date": report_data["date"]}


@celery_app.task(name="celery_tasks.beats.business.clear_expired_sessions")
def clear_expired_sessions():
    """
    清理过期会话

    每 30 分钟清理一次过期的用户会话
    """
    logger.info("[定时任务] 开始清理过期会话")

    # 模拟清理逻辑
    expired_count = 0
    # 实际应用中应该查询数据库并删除过期记录
    # sessions = Session.objects.filter(expire_time__lt=now())
    # expired_count = sessions.count()
    # sessions.delete()

    logger.success(f"[定时任务] 清理完成，共删除 {expired_count} 个过期会话")
    return {"cleaned_count": expired_count, "status": "success"}


@celery_app.task(name="celery_tasks.beats.business.sync_data_task")
def sync_data_task():
    """
    数据同步任务

    每小时同步一次外部数据
    """
    logger.info("[定时任务] 开始同步外部数据")

    try:
        # 模拟数据同步
        sync_start = datetime.now()

        # 这里应该放置实际的同步代码
        # - 调用第三方 API
        # - 更新本地数据库
        # - 处理增量数据

        sync_duration = (datetime.now() - sync_start).total_seconds()

        logger.success(f"[定时任务] 数据同步完成，耗时 {sync_duration:.2f}秒")
        return {
            "status": "success",
            "sync_time": sync_start.isoformat(),
            "duration": sync_duration
        }
    except Exception as e:
        logger.error(f"[定时任务] 数据同步失败：{str(e)}")
        return {"status": "failed", "error": str(e)}


@celery_app.task(name="celery_tasks.beats.business.backup_database")
def backup_database():
    """
    数据库备份任务

    每天凌晨 2 点执行数据库备份
    """
    logger.info("[定时任务] 开始数据库备份")

    try:
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{backup_time}.sql"

        # 模拟备份操作
        # 实际应用中应该：
        # 1. 执行数据库导出命令
        # 2. 压缩备份文件
        # 3. 上传到云存储
        # 4. 清理旧的备份文件

        logger.success(f"[定时任务] 数据库备份完成，文件名：{backup_file}")
        return {"status": "success", "backup_file": backup_file}
    except Exception as e:
        logger.error(f"[定时任务] 数据库备份失败：{str(e)}")
        return {"status": "failed", "error": str(e)}


@celery_app.task(name="celery_tasks.beats.business.calculate_statistics")
def calculate_statistics():
    """
    统计计算任务

    每 15 分钟计算一次实时统计数据
    """
    logger.info("[定时任务] 开始计算统计数据")

    # 模拟统计计算
    stats = {
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "page_views": 10000,
            "unique_visitors": 2500,
            "conversion_rate": 3.5,
            "average_order_value": 299.99,
        }
    }

    logger.info(f"统计数据：{stats}")
    logger.success("[定时任务] 统计计算完成")

    return {"status": "success", "statistics": stats}


@celery_app.task(name="celery_tasks.beats.business.notify_overdue_orders")
def notify_overdue_orders():
    """
    逾期订单提醒任务

    每天早上 10 点检查并发送逾期订单提醒
    """
    logger.info("[定时任务] 开始检查逾期订单")

    # 模拟查询逾期订单
    overdue_orders = []
    # 实际应用中应该：
    # overdue_orders = Order.objects.filter(
    #     status='pending',
    #     payment_deadline__lt=now()
    # )

    notified_count = 0
    for order in overdue_orders:
        # 发送邮件或短信提醒
        logger.info(f"发送逾期提醒：订单 {order.get('id', 'N/A')}")
        notified_count += 1

    logger.success(f"[定时任务] 逾期订单提醒完成，共通知 {notified_count} 个订单")
    return {
        "status": "success",
        "notified_count": notified_count,
        "total_overdue": len(overdue_orders)
    }
