import toml
import os

from loguru import logger


def load_toml(config_file: str):
    if not os.path.isfile(config_file):
        logger.warning(f"{config_file} not exists")
        return {}

    # 直接读取 toml 文件
    try:
        return toml.load(config_file)
    except Exception as e:
        logger.warning(f"{config_file} load error: {e}")

    # 尝试读取 utf-8-sig
    try:
        logger.info("trying to load as utf-8-sig")
        with open(config_file, mode="r", encoding='utf-8-sig') as fp:
            _cfg_content = fp.read()
            return toml.loads(_cfg_content)
    except Exception as e:
        logger.warning(f"{config_file} load as utf-8-sig error: {e}")

    return {}
