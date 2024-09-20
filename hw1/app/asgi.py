import json
from urllib.parse import parse_qs
from .math_functions import factorial, fibonacci
from .utils import send_json_response, get_body

async def handle_request(scope, receive, send):
    method = scope['method']
    path = scope['path']

    if method == 'GET' and path == '/factorial':
        await handle_factorial(scope, receive, send)
    elif method == 'GET' and path.startswith('/fibonacci/'):
        await handle_fibonacci(scope, receive, send)
    elif method == 'GET' and path == '/mean':
        await handle_mean(scope, receive, send)
    else:
        await send_json_response(send, 404, {"error": "Not Found"})

async def handle_factorial(scope, receive, send):
    query_string = scope['query_string']
    query_params = parse_qs(query_string.decode())
    n_values = query_params.get('n')

    if not n_values:
        await send_json_response(send, 422, {"error": "Unprocessable Entity"})
    else:
        try:
            n = int(n_values[0])
            if n < 0:
                await send_json_response(send, 400, {"error": "Bad Request"})
            else:
                result = factorial(n)
                await send_json_response(send, 200, {"result": result})
        except ValueError:
            await send_json_response(send, 422, {"error": "Unprocessable Entity"})

async def handle_fibonacci(scope, receive, send):
    path = scope['path']
    n_str = path[len('/fibonacci/'):]

    if not n_str:
        await send_json_response(send, 422, {"error": "Unprocessable Entity"})
    else:
        try:
            n = int(n_str)
            if n < 0:
                await send_json_response(send, 400, {"error": "Bad Request"})
            else:
                result = fibonacci(n)
                await send_json_response(send, 200, {"result": result})
        except ValueError:
            await send_json_response(send, 422, {"error": "Unprocessable Entity"})

async def handle_mean(scope, receive, send):
    request_body = await get_body(receive)

    try:
        data = json.loads(request_body.decode())
        if not isinstance(data, list):
            await send_json_response(send, 422, {"error": "Unprocessable Entity"})
        if not data:
            await send_json_response(send, 400, {"error": "Bad Request"})
        elif not all(isinstance(item, (int, float)) for item in data):
            await send_json_response(send, 400, {"error": "Bad Request"})
        else:
            result = sum(data) / len(data)
            await send_json_response(send, 200, {"result": result})
    except json.JSONDecodeError:
        await send_json_response(send, 422, {"error": "Unprocessable Entity"})
    except ValueError as e:
        await send_json_response(send, 422, {"error": "Unprocessable Entity"})
