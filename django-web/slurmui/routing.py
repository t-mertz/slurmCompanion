from channels.routing import route
from webcmd.consumers import ssh_cmd

channel_routing = [
    #route("http.request", "myapp.consumers.http_consumer"),
    route("websocket.receive", ssh_cmd),
]