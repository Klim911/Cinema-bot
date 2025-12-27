from .hendlers_main import router as router_handlers_main
from .hendlers_search import router as router_handlers_search
from .hendlers_top import router as router_handlers_top
from .hendlers_random import router as router_handlers_random
from .hendlers_favorites import router as router_handlers_favorites

routers = [
    router_handlers_main,
    router_handlers_search,
    router_handlers_top,
    router_handlers_random,
    router_handlers_favorites
]