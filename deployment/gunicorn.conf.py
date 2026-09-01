import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5

# Log to stdout/stderr so Render (and Docker) captures logs centrally
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
