import json

from flask import Flask, request, abort
from providers.openserve import OpenServe

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    TESTING=True
)

openserve = OpenServe()


def response_handler(data):
    candidates = data.get('candidates')[0]
    address = candidates.get('address')
    latitude = candidates.get('location').get('y')
    longitude = candidates.get('location').get('x')

    response = {'event': 'response',
                'providers': []}

    result = openserve.services_available(address, latitude, longitude)

    if not isinstance(result, int):
        response['providers'].append(result)
        return json.dumps(response)
    else:
        abort(result)


@app.route('/api/v1', methods=['POST'])
def request_handler():
    try:
        data = json.loads(request.get_data(as_text=True))
        result = openserve.geocoding(data)

        if not isinstance(result, int):
            decoded = json.loads(result.data.decode('utf-8'))
            result = response_handler(decoded)

            if not isinstance(result, int):
                return result
            else:
                abort(result)
        else:
            abort(result)
    except json.JSONDecodeError:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
