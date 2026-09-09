import aioredis

import app.config as config

token_blocklist = aioredis.StrictRedis(
    host=config.redis_host,
    port=config.redis_port,
    db=config.redis_db
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(jti, "", ex=config.redis_jti_expiry_seconds)


async def token_in_blocklisted(jti: str) -> bool:
    return await token_blocklist.exists(jti)
