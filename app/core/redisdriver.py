import redis
import os

_redis_client = None

def get_client() :
	""" Get redis client singleton object
	"""
	global _redis_client
	if _redis_client: return _redis_client
	else :
		_redis_client = redis.StrictRedis(
			host=os.environ.get('REDIS_HOST', 'localhost'),
			port=int(os.environ.get('REDIS_PORT', '6000')),
			db=0
		)
		return _redis_client