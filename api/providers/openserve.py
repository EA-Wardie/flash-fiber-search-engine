import json

import handler


class OpenServe:
    def __init__(self):
        self.url = 'https://gis.telkom.co.za'
        self.techapiv2 = '/apps/api/ucmTechAPIV2'

        self.headers = {'Host': 'gis.telkom.co.za',
                        'Referer': 'https://openserve.co.za/opencoveragemap/support/check-coverage',
                        'Origin': 'https://openserve.co.za'}

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
                                if 'errorCode' in result:
                                    if result.get('errorCode') == 0:
                                        items = result.get('results').get('items').pop(0)
                                        if 'payload' in items:
                                            payload = items['payload']

                                            response = {'id': 0,
                                                        'company': 'Openserve',
                                                        'logo': 'https://openserve.co.za/open/assets/_images/'
                                                                'openserve_logo.svg',
                                                        'ftth': 'Unknown',
                                                        'status': 'Unknown'}

                                            if 'FTTHBoundary' in payload:
                                                ftth = payload.get('FTTHBoundary')
                                                response['ftth'] = ftth

                                            if 'ftthInfrastructure' in payload:
                                                ftth_info = payload.get('ftthInfrastructure').get('ftthInfo').pop(0)
                                                if 'FTTH_Status' in ftth_info:
                                                    status = ftth_info.get('FTTH_Status')
                                                    response['status'] = status

                                            return response

                                else:
                                    return {'event': 'error', 'msg': 'incomplete response'}
                        else:
                            return {'event': 'error', 'msg': 'unknown error', 'code': status}

                else:
                    return {'event': 'error', 'msg': 'incomplete response'}
        else:
            return {'event': 'error', 'msg': 'unknown error', 'code': status}
