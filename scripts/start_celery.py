#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Celery 统一启动脚本

支持多种运行模式：
- worker: 仅启动 Celery Worker
- beat: 仅启动 Celery Beat
- all: 同时启动 Worker + Beat

使用方法:
    python scripts/start_celery.py worker    # 启动 Worker
    python scripts/start_celery.py beat      # 启动 Beat
    python scripts/start_celery.py all       # 启动 Worker + Beat

参数:
    --loglevel    日志级别 (DEBUG, INFO, WARNING, ERROR), 默认 INFO
    --pool        进程池类型 (solo, prefork, eventlet, gevent), 默认 solo (Windows)

示例:
    python scripts/start_celery.py worker --loglevel=DEBUG
    python scripts/start_celery.py all --pool=prefork
"""

import sys
import subprocess
import platform
import socket
from pathlib import Path


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.parent


def check_python_environment():
    """检查 Python 环境"""
    print("=" * 50)
    print("Celery 统一启动脚本")
    print("=" * 50)
    print()

    python_version = sys.version
    print(f"[信息] Python 版本：{python_version.split()[0]}")

    # 检查是否在虚拟环境中
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"[信息] 当前在虚拟环境中：{sys.prefix}")
    else:
        print(f"[警告] 未检测到虚拟环境，建议使用 uv run 运行此脚本")
        print(f"[提示] 示例：uv run python scripts/start_celery.py worker")
    print()


def check_redis_connection(host: str = "localhost", port: int = 6379) -> bool:
    """检查 Redis 连接"""
    print("[信息] 检查 Redis 连接...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print(f"[成功] Redis 连接正常 ({host}:{port})")
            return True
        else:
            print(f"[警告] 无法连接到 Redis ({host}:{port})")
            raise ConnectionError(f"Redis 端口 {port} 未开放")
    except Exception as e:
        print(f"[警告] Redis 连接失败：{e}")
        print("[提示] 请确保 Redis 服务已启动")
        print("[提示] 或使用 Docker 启动:")
        print("  docker run -d -p 6379:6379 redis:latest")
        print()
        return False


def get_default_pool() -> str:
    """根据操作系统获取默认的进程池类型"""
    system = platform.system()
    if system == "Windows":
        return "solo"
    else:
        return "prefork"


def build_celery_command(mode: str, loglevel: str, pool: str) -> list:
    """构建 Celery 启动命令"""
    celery_app = "celery_tasks.celery_app"  # 指定 Celery 应用实例

    # 基础命令
    cmd = ["celery"]

    if mode == "worker":
        cmd.extend(["-A", celery_app, "worker", f"--loglevel={loglevel}"])
        if pool:
            cmd.append(f"--pool={pool}")
        else:
            # Windows 默认使用 solo
            default_pool = get_default_pool()
            cmd.append(f"--pool={default_pool}")
            print(f"[信息] 使用默认进程池：{default_pool}")

    elif mode == "beat":
        cmd.extend(["-A", celery_app, "beat", f"--loglevel={loglevel}"])

    elif mode == "all":
        # Windows 不支持 --beat 参数，需要分别启动
        if platform.system() == "Windows":
            print("[信息] Windows 系统需要分别启动 Worker 和 Beat")
            print("[提示] 请运行以下两个命令：")
            print("  python scripts/start_celery.py worker")
            print("  python scripts/start_celery.py beat")
            print()
            # 在 Windows 上，all 模式只启动 Worker
            cmd.extend(["-A", celery_app, "worker", f"--loglevel={loglevel}"])
            if pool:
                cmd.append(f"--pool={pool}")
            else:
                default_pool = get_default_pool()
                cmd.append(f"--pool={default_pool}")
                print(f"[信息] 使用默认进程池：{default_pool}")
        else:
            cmd.extend(["-A", celery_app, "worker",
                       "--beat", f"--loglevel={loglevel}"])
            if pool:
                cmd.append(f"--pool={pool}")
            else:
                default_pool = get_default_pool()
                cmd.append(f"--pool={default_pool}")
                print(f"[信息] 使用默认进程池：{default_pool}")
    else:
        raise ValueError(f"未知的运行模式：{mode}")

    return cmd


def print_startup_info(mode: str, loglevel: str, pool: str):
    """打印启动信息"""
    print()
    print("=" * 50)

    mode_names = {
        "worker": "Celery Worker",
        "beat": "Celery Beat 调度器",
        "all": "Celery Worker + Beat 一体化"
    }

    print(f"启动模式：{mode_names.get(mode, mode)}")
    print(f"日志级别：{loglevel}")
    if pool:
        print(f"进程池：{pool}")
    print()

    if mode == "worker":
        print("功能：处理异步任务")
    elif mode == "beat":
        print("功能：定时任务调度（需要配合 Worker 使用）")
    elif mode == "all":
        if platform.system() == "Windows":
            print("功能：同时启动 Worker + Beat（双进程模式）")
            print("说明：Windows 将自动启动两个独立进程")
        else:
            print("功能：同时处理任务和调度（适合开发和测试）")

    print()
    print("按 Ctrl+C 停止服务")
    print("=" * 50)
    print()


def run_celery(cmd: list):
    """运行 Celery 命令"""
    print(f"[信息] 执行命令：{' '.join(cmd)}")
    print()

    try:
        # 使用 subprocess.run 直接运行，允许用户交互
        process = subprocess.run(cmd, cwd=get_project_root())

        if process.returncode != 0:
            print()
            print("[错误] Celery 启动失败")
            print("[提示] 检查上方的错误信息")
            return False
        return True

    except KeyboardInterrupt:
        print()
        print("[信息] 用户中断，正在停止服务...")
        return True
    except FileNotFoundError as e:
        print()
        print(f"[错误] 找不到命令：{e}")
        print("[提示] 确保 Celery 已安装且在正确的虚拟环境中")
        return False
    except Exception as e:
        print()
        print(f"[错误] 发生未知错误：{e}")
        return False


def run_celery_windows_all(loglevel: str, pool: str):
    """在 Windows 上同时启动 Worker 和 Beat（两个独立进程）"""
    import time

    project_root_str = str(get_project_root())
    script_path = Path(project_root_str) / "scripts" / "start_celery.py"

    print("[信息] Windows 系统将启动两个独立进程...")
    print(f"[信息] Worker 进程：celery worker --loglevel={loglevel}")
    print(f"[信息] Beat 进程：celery beat --loglevel={loglevel}")
    print()

    # 启动 Worker 进程（后台运行）
    worker_cmd = [
        sys.executable,
        str(script_path),
        "worker",
        f"--loglevel={loglevel}",
        f"--pool={pool if pool else 'solo'}",
        "--skip-redis-check"
    ]

    # 启动 Beat 进程（后台运行）
    beat_cmd = [
        sys.executable,
        str(script_path),
        "beat",
        f"--loglevel={loglevel}",
        "--skip-redis-check"
    ]

    try:
        # 使用 subprocess.Popen 启动两个后台进程
        worker_process = subprocess.Popen(worker_cmd, cwd=project_root_str)
        time.sleep(2)  # 等待 2 秒，让 Worker 先启动
        beat_process = subprocess.Popen(beat_cmd, cwd=project_root_str)

        print("[成功] Worker 和 Beat 都已启动")
        print("[提示] 按 Ctrl+C 将停止所有进程")
        print()

        # 等待用户中断
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print()
        print("[信息] 用户中断，正在停止所有服务...")
        worker_process.terminate()
        beat_process.terminate()
        worker_process.wait(timeout=5)
        beat_process.wait(timeout=5)
        print("[成功] 所有服务已停止")
        return True
    except Exception as e:
        print()
        print(f"[错误] 启动失败：{e}")
        return False


def parse_args():
    """解析命令行参数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Celery 统一启动脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/start_celery.py worker          启动 Worker (Windows 自动使用 solo 模式)
  python scripts/start_celery.py beat            启动 Beat 调度器
  python scripts/start_celery.py all             启动 Worker + Beat (仅 Linux/Mac)
  python scripts/start_celery.py worker --loglevel=DEBUG  使用 DEBUG 日志级别
  python scripts/start_celery.py all --pool=prefork      使用 prefork 进程池 (Linux/Mac)

注意:
  - Windows 系统必须使用 --pool=solo
  - Windows 系统不支持 all 模式 (--beat)，请分别启动 worker 和 beat
  - Linux/Mac 系统推荐使用 --pool=prefork
  - 建议先启动 Redis 服务：docker run -d -p 6379:6379 redis:latest
        """
    )

    parser.add_argument(
        "mode",
        choices=["worker", "beat", "all"],
        help="运行模式：worker(仅 Worker), beat(仅 Beat), all(Worker+Beat，Linux/Mac 专用)"
    )

    parser.add_argument(
        "--loglevel",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="日志级别 (默认：INFO)"
    )

    parser.add_argument(
        "--pool",
        type=str,
        default=None,
        choices=["solo", "prefork", "eventlet", "gevent"],
        help="进程池类型 (默认：Windows 使用 solo, 其他使用 prefork)"
    )

    parser.add_argument(
        "--skip-redis-check",
        action="store_true",
        help="跳过 Redis 连接检查"
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 检查 Python 环境
    check_python_environment()

    # 检查 Redis 连接（除非跳过）
    if not args.skip_redis_check:
        redis_ok = check_redis_connection()
        if not redis_ok:
            print("[警告] 继续启动流程，但 Celery 可能无法正常工作")
            print()

    # Windows 特殊处理：all 模式需要启动两个独立进程
    if args.mode == "all" and platform.system() == "Windows":
        print_startup_info(args.mode, args.loglevel, args.pool)
        default_pool = args.pool if args.pool else get_default_pool()
        success = run_celery_windows_all(args.loglevel, default_pool)
        sys.exit(0 if success else 1)
        return

    # 打印启动信息
    print_startup_info(args.mode, args.loglevel, args.pool)

    # 构建命令
    cmd = build_celery_command(args.mode, args.loglevel, args.pool)

    # 运行 Celery
    success = run_celery(cmd)

    # 退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
