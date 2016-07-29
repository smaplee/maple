from subprocess import PIPE, Popen
# from tornado.log import app_log
import time
import os


def stdout(cmd, env=None, timeout=30):
    if env is None:
        env = os.environ
    process = Popen(cmd, env=env, shell=True, stderr=PIPE, stdout=PIPE)
    deadline = int(time.time()) + int(timeout)
    ret = 1
    errput = ''
    output = ''
    while True:
        if int(time.time()) < deadline:
            result = process.poll()
            if result is None:
                time.sleep(3)
            else:
                ret = result
                errput = process.stderr.read()
                output = process.stdout.read()
                # app_log.error(elog)
                process.stderr.close()
                break
        else:
            process.kill()
            break
    return ret, output


def retcode(cmd, env=None, timeout=30):
    ret,_ = stdout(cmd, env, timeout=30)
    return ret

