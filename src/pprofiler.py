import cProfile, pstats
from functools import wraps, partial


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parameterized
def pprof(f, sort_by="ncalls", line_to_print=None, strip_dirs=False):
    @wraps(f)
    def wrapper(*args, **kwargs):
        profiler = Profiler()
        profiler.start()
        result = f(*args, **kwargs)
        profiler.stop()
        profiler.print()
        return result

    return wrapper


class Profiler:
    def __init__(self):
        self._profiler = cProfile.Profile()

    def start(self):
        self._profiler.enable()

    def stop(self):
        self._profiler.disable()

    def print(self, sort_by="ncalls", line_to_print=None, strip_dirs=False):
        stats = pstats.Stats(self._profiler)
        if strip_dirs:
            stats.strip_dirs()

        if isinstance(sort_by, (tuple, list)):
            stats.sort_stats(*sort_by)
        else:
            stats.sort_stats(sort_by)
        stats.print_stats(line_to_print)
