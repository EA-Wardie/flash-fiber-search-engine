import json

import handler


class Geocoding:
    def __init__(self):
        self.url = 'https://gis.telkom.co.za'
        self.geocode = '/locators/rest/services/Telkom_Composite/GeocodeServer/findAddressCandidates'

        self.headers = {'Host': 'gis.telkom.co.za',
                        'Referer': 'https://openserve.co.za/opencoveragemap/support/check-coverage',
                        'Origin': 'https://openserve.co.za'}

    async def geocoding(self, session, data):
        text = data.get('text')
        magic_key = data.get('magicKey')

        if text and magic_key:
            params = {'SingleLine': text,
                      'f': 'json',
                      'magicKey': magic_key,
                      'maxLocations': 1}

            result, status = await handler.myrequest(session, 'GET', self.url + self.geocode,
                                                     params=params, headers=self.headers)

            if status == 200:
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    return {'event': 'error', 'msg': 'invalid json'}
                else:
                    if 'candidates' in result:
                        candidates = result.get('candidates').pop(0)
                        if 'location' in candidates:
                            location = candidates.get('location')

                            return candidates['address'], location['y'], location['x']

                    return {'event': 'error', 'msg': 'invalid response'}
            else:
                return {'event': 'error', 'msg': 'unknown error', 'code': status}
        else:
            return {'event': 'error', 'msg': 'invalid request'}
