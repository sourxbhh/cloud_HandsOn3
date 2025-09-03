import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    """
    Connects to Redis and increments the 'hits' counter.
    Includes a retry mechanism for connection errors.
    """
    retries = 5
    while True:
        try:
            # The decode_responses=True argument makes the client return strings instead of bytes.
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    """
    Flask route that displays the hit count.
    """
    count = get_hit_count()
    # Using an f-string is a more modern and readable way to format strings.
    return f'Hello World! I have been seen {count} times.\n'

if __name__ == "__main__":
    # This block allows you to run the app directly for testing.
    app.run(host="0.0.0.0", port=5000, debug=True)
