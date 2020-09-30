from flask import Flask

from providers.providers import ProviderLookup

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    TESTING=True
)

lookup = ProviderLookup()


@app.route('/', methods=['GET'])
def index():
    return ''


@app.route('/api/v1', methods=['POST'])
def api_handler():
    p = lookup.get_providers('vumatel')
    p.download_mapdata()
    return ''


if __name__ == '__main__':
    app.run(debug=True)
