import asyncio
import json

from flask import Flask, request

from handler import MessageHandler

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    TESTING=True
)

message = MessageHandler()


@app.route('/api/v1', methods=['POST'])
def request_handler():
    try:
        data = request.get_data()
        eventl = asyncio.new_event_loop()
        result = eventl.run_until_complete(asyncio.wait_for(message.response_handler(data), timeout=10))
        eventl.close()
    except (RuntimeError, asyncio.TimeoutError):
        return json.dumps({'event': 'timeout'})

    return json.dumps(result)
    # try:
    #     data = json.loads(request.get_data(as_text=True))
    #     result = openserve.geocoding(data)
    #
    #     if not isinstance(result, int):
    #         decoded = json.loads(result.data.decode('utf-8'))
    #         result = response_handler(decoded)
    #
    #         if not isinstance(result, int):
    #             return result
    #         else:
    #             abort(result)
    #     else:
    #         abort(result)
    # except json.JSONDecodeError:
    #     abort(400)


if __name__ == '__main__':
    app.run()
