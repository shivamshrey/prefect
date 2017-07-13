import datetime
import dateutil


def retry_delay(
        interval=None,
        *,
        exponential_backoff=False,
        max_delay=datetime.timedelta(hours=2),
        **kwargs):
    """
    A helper function for generating task retry delays.

    Args:
        interval (timedelta): The amount of time to wait.
            This value is optional; users can also instantiate a new interval
            by passing keyword arguments directly to retry_delay. So:
                retry_delay(interval=timedelta(days=1))
            is equivalent to:
                retry_delay(days=1)

        **kwargs: Keyword arguments are passed to timedelta and
            are compatible with the datetime.timedelta API.

        exponential_backoff: if True, each retry delay will be exponentially
            longer than the last, starting with the second retry. For example,
            if the retry delay is 1 minute, then:
                - first retry starts after 1 minute
                - second retry also starts after 1 minute (no backoff applied)
                - third retry starts after 2 minutes
                - fourth retry starts after 4 minutes
                - etc.

        max_delay (timedelta): If exponential_backoff is supplied,
            delays will be capped by this amount.
    """
    if interval is not None and kwargs:
        raise ValueError(
            'Provide an interval or interval keywords, but not both.')
    elif interval is None and not kwargs:
        raise ValueError('Provide either an interval or interval keywords.')
    elif kwargs:
        interval = datetime.timedelta(**kwargs)

    def retry_delay(run_number):
        if exponential_backoff:
            scale = 2 ** (max(0, run_number - 2))
        else:
            scale = 1
        if max_delay is not None:
            return min(interval * scale, max_delay)
        else:
            return interval * scale

    return retry_delay

def parse_datetime(dt):
    """
    Parses a string, bytes, float, or datetime object and returns a
    corresponding datetime
    """
    if isinstance(dt, (str, bytes)):
        return dateutil.parser.parse(dt)
    elif isinstance(dt, float):
        return datetime.datetime.fromtimestamp(dt)
    elif isinstance(dt, (datetime.datetime)):
        return dt
    else:
        raise TypeError(
            'Unrecognized datetime input: {}'.format(type(dt).__name__))
