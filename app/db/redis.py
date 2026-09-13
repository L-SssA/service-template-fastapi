import redis.asyncio as aioredis

import app.config as config

token_blocklist = aioredis.from_url(config.redis_url)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(jti, "", ex=config.redis_jti_expiry_seconds)


async def token_in_blocklisted(jti: str) -> bool:
    return await token_blocklist.exists(jti)
