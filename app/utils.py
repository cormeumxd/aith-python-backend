import json

async def send_json_response(send, status, content):
    headers = [(b'content-type', b'application/json')]
    body = json.dumps(content).encode()

    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': headers,
    })

    await send({
        'type': 'http.response.body',
        'body': body,
    })

async def get_body(receive):
    more_body = True
    body = []

    while more_body:
        message = await receive()
        body.append(message.get('body', b''))
        more_body = message.get('more_body', False)

    return b''.join(body)