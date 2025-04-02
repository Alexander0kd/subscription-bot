from .commands import router as commands_router
from .messages import router as messages_router
from .callbacks import router as callbacks_router
from .errors import router as errors_router

routers = [
    commands_router,
    messages_router,
    callbacks_router,
    errors_router
]