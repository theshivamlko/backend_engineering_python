
from redis import Redis
from config import redis_settings

_blacklist = Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=0)

# print(_blacklist.ping())

async  def add_jti_to_blacklist(jti: str):
    """
    Add a JWT ID (jti) to the Redis blacklist with an expiration time.
    """
    _blacklist.set(jti,  "blacklisted")

async def is_jti_blacklisted(jti: str):
    """
    Check if a JWT ID (jti) is in the Redis blacklist.
    """
    return _blacklist.exists(jti)