from collections import deque
from app.models import Priority
from threading import Lock

queue = {p: deque() for p in Priority}
requests = {}
batches = {}
lock = Lock()
