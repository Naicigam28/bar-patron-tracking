"""All basic Redis operations are defined here."""
import redis
from fastapi.logger import logger
import json
from app.utils.settings import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
)

def set_key(key: str, value: dict) -> None:
    """Set a key-value pair in Redis."""
    try:
        logger.info(f"Setting key: {key} with value: {value} from Redis")
        value_str = json.dumps(value)
        redis_client.set(key, value_str)
    except Exception as e:
        logger.error(f"Error setting key: {key} with value: {value} from Redis")
        logger.error(e)

def get_key(key: str) -> dict:
    """Get a value from Redis by key."""
    try:
        logger.info(f"Getting value for key: {key} from Redis")
        value_str=redis_client.get(key)
        if value_str is None:
            return None
        value_dict=json.loads(value_str)
        if value_dict is None or len(value_dict)==0:
            return None
        return value_dict
    except Exception as e:
        logger.error(f"Error getting value for key: {key} from Redis")
        logger.error(e)
        return None

    
