import json

import handler


class OpenServe:
    def __init__(self):
        self.url = 'https://gis.telkom.co.za'
        self.techapiv2 = '/apps/api/ucmTechAPIV2'

        self.headers = {'Host': 'gis.telkom.co.za',
                        'Referer': 'https://openserve.co.za/opencoveragemap/support/check-coverage',
                        'Origin': 'https://openserve.co.za'}

    def decode_json(self, data):
        ftth = 'No'
        status = 'Unknown'
        if 'results' in data:
            results = data['results']['items']
            for result in results:
                if 'payload' in result:
                    payload = result['payload']
                    for item in payload:
                        if 'FTTHBoundary' in item:
                            ftth = payload[item]

                        if 'ftthInfrastructure' in item:
                            infrastructure = payload[item]
                            for status in infrastructure:
                                if 'ftthInfo' in status:
                                    ftth_info = infrastructure[status]
                                    for keys in ftth_info:
                                        for key in keys:
                                            if 'FTTH_Status' in key:
                                                status = keys[key]
        return ftth, status

    async def fetch_services(self, session, address, latitude, longitude):
        params = {'LAT': latitude,
                  'LON': longitude,
                  'ADDRESS': address,
                  'GCACCURACY': 'ROOFTOP'}

        result, status = await handler.myrequest(session, 'GET', self.url + self.techapiv2,
                                                 params=params, headers=self.headers)

        if status == 200:
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                return {'event': 'error', 'msg': 'invalid json'}
            else:
                if 'AddressVerify' in result:
                    verified = result.get('AddressVerify').pop(0)

                    if verified:
                        latitude = verified.get('LR_LAT')
                        longitude = verified.get('LR_LON')
                        address = verified.get('LR_Address')
                        amid = verified.get('AMID')

                        params = {'LAT': latitude,
                                  'LON': longitude,
                                  'ADDRESS': address,
                                  'AMID': amid,
                                  'GCACCURACY': 'VERIFIED'}

                        result, status = await handler.myrequest(session, 'GET', self.url + self.techapiv2,
                                                                 params=params, headers=self.headers)

                        if status == 200:
                            try:
                                result = json.loads(result)
                            except json.JSONDecodeError:
                                return {'event': 'error', 'msg': 'invalid json'}
                            else:
                                ftth, status = self.decode_json(result)

                                response = {'company': 'Openserve',
                                            'logo': 'https://openserve.co.za/open/assets/_images/'
                                                    'openserve_logo.svg',
                                            'ftth': ftth,
                                            'status': status}

                                return response

                        else:
                            return {'event': 'error', 'msg': 'geolocation error', 'code': status}

        else:
            return {'event': 'error', 'msg': 'geolocation error', 'code': status}
