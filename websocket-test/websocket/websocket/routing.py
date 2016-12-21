from channels.routing import route
from myapp.consumers import ws_message

channel_routing = [
    #route("http.request", "myapp.consumers.http_consumer"),
    route("websocket.receive", ws_message),
]