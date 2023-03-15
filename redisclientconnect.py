import redis


class RedisClient:
    """
        we define a RedisClient class using the singleton pattern. The class has a _instance variable that stores the single instance of the Redis client.
        The __new__ method checks if an instance of the class has already been created, and if not, creates a new instance of the Redis client.
        We then create an instance of the RedisClient class and store it in the redis_client variable, which we make a global variable.
        Finally, in the route function, we access the Redis client using the redis_client variable and use it to get a value from Redis.
        By creating a single instance of the Redis client and storing it in a global variable, we can access it from any route in the FastAPI application.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = redis.Redis(host='localhost',port=6379,db=0) 
            # print("connection true")
        return cls._instance