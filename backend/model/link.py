from backend.persistence.redis import redis_client
from backend.model.user import User


class Link(object):
    """
    Represents a link (in redis) between a randomly genereated frontend id and a user id
    """

    @staticmethod
    def key_for_token(token):
        return "link:{}".format(token)

    @staticmethod
    def create(token, user_id):
        redis_client.set(Link.key_for_id(), user_id)
        return Link(token, user_id)

    @staticmethod
    def query(token):
        uid = redis_client.get(Link.key_for_token(token))
        if uid is None:
            return uid

        return Link(token, uid)

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    @property
    def user(self):
        return User.query.get(self.user_id).first()
