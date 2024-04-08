import inspect

YELLOW = "\033[33m"
RED    = "\033[31m"
WHITE  = "\033[37m"
CLR    = "\033[0m"

def disp(strfmt, *args ,level=0):
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    fname = caller.filename.replace("\\", "/").split("/")[-1]
    print(f"[{fname} {[WHITE, YELLOW, RED][level]}{['INFO', 'WARN', 'FATAL'][level]}{CLR}] - "+strfmt.format(*args))
    if level == 2:
        exit(1)