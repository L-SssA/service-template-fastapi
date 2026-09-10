import argparse
import subprocess

def parse_args():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="alembic 助手工具")

    subparsers = parser.add_subparsers(
        dest="action", required=True, help="要执行的操作")

    # ============= commit =============
    commit_parser = subparsers.add_parser("commit", help="生成迁移脚本")
    commit_parser.add_argument("message", help="迁移脚本描述")

    # ============= upgrade =============
    upgrade_parser = subparsers.add_parser("up", help="升级数据库")
    upgrade_parser.add_argument(
        "revision", nargs="?", default="head", help="目标版本号，head 代表最新版本号")

    # ============= downgrade =============
    downgrade_parser = subparsers.add_parser("down", help="降级数据库")
    downgrade_parser.add_argument(
        "revision", nargs="?", default="-1", help="回滚到哪个版本，例如：-1 或 base")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    if args.action == "commit":
        print(f"alembic commit: {args.message}")
        subprocess.run(
            [
                "alembic", "revision",
                "--autogenerate",
                "-m", args.message
            ]
        )
    elif args.action == "up":
        print(f"alembic upgrade: {args.revision}")
        subprocess.run(["alembic", "upgrade", args.revision])
    elif args.action == "down":
        print(f"alembic downgrade: {args.revision}")
        subprocess.run(["alembic", "downgrade", args.revision])
