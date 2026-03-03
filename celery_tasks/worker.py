"""
Celery Worker 启动入口文件

使用示例:
    celery -A celery_tasks.worker worker --loglevel=info --pool=solo
    
Windows 环境必须使用 --pool=solo 参数
"""

from . import celery_app

# 导出 Celery 实例，供命令行工具使用
app = celery_app

if __name__ == "__main__":
    # 直接运行此文件时启动 worker
    app.start()
