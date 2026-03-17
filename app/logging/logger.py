import os
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Callable, Dict, Any

COLOR_MAP = {
    "INFO": "\033[94m",
    "WARNING": "\033[93m",
    "ERROR": "\033[92m",
    "DEBUG": "\033[91m",
    "RESET": "\033[0m",
}

log_queue = []

def log(level, message, method, block, status):
    timestamp = datetime.now.strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "level" : level,
        "timestamp" : timestamp,
        "message" : message,
        "method" : method,
        "block" : block,
        "status" : status,
    }