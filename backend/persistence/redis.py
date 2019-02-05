from redis import Redis


class RedisClient(object):

    def __init__(self, app=None, **kwargs):
        self._redis_client = None
        self.provider_kwargs = kwargs

        if app is not None:
            self.init_app(app)

    def init_app(self, app, **kwargs):
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')

        self._redis_client = Redis.from_url(
            redis_url, **self.provider_kwargs
        )

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['redis'] = self

    def get(self, name, default=None):
        res = self._redis_client.get(name)
        if res is None:
            return default
        return res.decode()

    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    # def __getitem__(self, name):
    #     return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]


redis_client = RedisClient()


def init_app(app):
    redis_client.init_app(app)
