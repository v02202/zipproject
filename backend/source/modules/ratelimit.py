from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=1, period=60)
def rateLimit():
    return