import multiprocessing
import os
# Server socket
bind = os.environ['VAULT_HOST'] + ":" + os.environ['VAULT_PORT']
workers = multiprocessing.cpu_count() * 2 + 1

# Logging
_logdir = os.environ['VAULT_LOGS_DIR']

accesslog = _logdir + "/access.log"  # specify the path to the access log file
errorlog = _logdir + "/error.log"  # specify the path to the error log file
logfile = _logdir + "/server.log"

loglevel = "info"
access_log_format = '%({X-Forwarded-For}i)s [%(h)s] %(l)s %(u)s %(t)s "%(r)s" -> {%(s)s -> len(%(b)s)} "%(f)s";"%(a)s"'

# Worker processes
timeout = 4
keepalive = 2
