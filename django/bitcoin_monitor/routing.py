from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import blocks.urls
import prices.urls


websocket_urlpatterns = (
    blocks.urls.websocket_urlpatterns + prices.urls.websocket_urlpatterns
)

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))}
)
