import asyncio
import json
import time

from flask import Flask, request

from handler import MessageHandler

app = Flask(__name__)
app.config['ENV'] = 'development'

message = MessageHandler()


@app.route('/api/v1', methods=['POST'])
def request_handler():
    try:
        data = request.get_data()
        eventl = asyncio.new_event_loop()
        result = eventl.run_until_complete(asyncio.wait_for(message.response_handler(data), timeout=10))
    except (RuntimeError, asyncio.TimeoutError):
        return json.dumps({'event': 'timeout'})

    return json.dumps(result)


if __name__ == '__main__':
    app.run()
    time.sleep(0.1)
