# Helper code: https://stackoverflow.com/questions/31663288/how-do-i-properly-use-connection-pools-in-redis
import redis

redis_pool = None 

def init():
    global redis_pool
    redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

redis_client_ = redis.Redis(connection_pool=redis_pool, decode_responses=True)
