@echo off
REM Celery Worker 启动脚本 (Windows)
REM 
REM 使用方法:
REM   .\start_celery_worker.bat
REM
REM 参数:
REM   --loglevel=INFO  设置日志级别 (DEBUG, INFO, WARNING, ERROR)
REM   --pool=solo      Windows 必须使用 solo 模式

echo ========================================
echo Celery Worker 启动脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请确保已安装并添加到 PATH
    pause
    exit /b 1
)

echo [信息] 检测 Python 环境...
python --version
echo.

REM 检查 Redis 连接
echo [信息] 检查 Redis 连接...
powershell -Command "Test-NetConnection -ComputerName localhost -Port 6379 -InformationLevel Quiet" >nul 2>&1
if errorlevel 1 (
    echo [警告] 无法连接到 Redis (端口 6379)
    echo [提示] 请确保 Redis 服务已启动，或使用 Docker 启动：
    echo   docker run -d -p 6379:6379 redis:latest
    echo.
) else (
    echo [成功] Redis 连接正常
)
echo.

REM 启动 Celery Worker
echo ========================================
echo 启动 Celery Worker...
echo ========================================
echo.
echo 命令：celery -A celery_tasks.worker worker --loglevel=info --pool=solo
echo.
echo 按 Ctrl+C 停止 Worker
echo.

celery -A celery_tasks.worker worker --loglevel=info --pool=solo

if errorlevel 1 (
    echo.
    echo [错误] Celery Worker 启动失败
    echo [提示] 检查上方的错误信息
    pause
    exit /b 1
)
