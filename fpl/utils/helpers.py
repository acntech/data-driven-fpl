"""Helper functions with no other home."""
import time


def timer(func):
    """Print execution time of a function."""

    def wrapper_timer(*args, print_time=True, **kwargs):
        start = time.time()
        temp = func(*args, **kwargs)
        if print_time:
            print(f"Execution of {func.__name__} took {time.time() - start}")
        return temp

    return wrapper_timer
