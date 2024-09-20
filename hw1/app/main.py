from .asgi import handle_request

async def app(scope, receive, send):
    assert scope['type'] == 'http'
    
    await handle_request(scope, receive, send)