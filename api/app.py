from flask import Flask

from providers.providers import ProviderLookup

app = Flask(__name__)
lookup = ProviderLookup()


@app.route('/api/v1', methods=['POST'])
def api_handler():
    p = lookup.get_providers('vumatel')
    p.download_mapdata()
    return ''


if __name__ == '__main__':
    app.run(debug=True)
