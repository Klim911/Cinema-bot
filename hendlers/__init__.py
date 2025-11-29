from .hendlers_main import router as router_handlers_main
from .hendlers_search import router as router_handlers_search

routers = [
    router_handlers_main,
    router_handlers_search
]