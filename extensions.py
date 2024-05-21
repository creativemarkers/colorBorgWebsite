from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def defaultErrorResponder(something):
    print(something)
    print("limit exceeded")
    print(limiter.current_limit.limit)
    print(get_remote_address())

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="memory://",
    on_breach=defaultErrorResponder
)
