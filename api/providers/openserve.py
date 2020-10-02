import json
import urllib3


class OpenServe:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.url = 'https://gis.telkom.co.za'
        self.findaddress = '/locators/rest/services/Telkom_Composite/GeocodeServer/findAddressCandidates'
        self.techapiv2 = '/apps/api/ucmTechAPIV2'

    def geocoding(self, data):
        headers = {'Host': 'gis.telkom.co.za',
                   'Referer': 'https://openserve.co.za/opencoveragemap/support/check-coverage',
                   'Origin': 'https://openserve.co.za'}

        text = data.get('text')
        magic_key = data.get('magicKey')

        if text and magic_key:
            fields = {'SingleLine': text,
                      'f': 'json',
                      # 'outFields': 'Match_addr,Loc_name,Addr_type,AddNum,StAddr,StName,'
                      # 'StType,Nbrhd,City,Region,Postal,Country',
                      'magicKey': magic_key,
                      'maxLocations': 1}

            return self.http.request('GET', self.url + self.findaddress, headers=headers, fields=fields)
        else:
            return 400

    def services_available(self, address, latitude, longitude):
        headers = {'Host': 'gis.telkom.co.za',
                   'Referer': 'https://openserve.co.za/opencoveragemap/support/check-coverage',
                   'Origin': 'https://openserve.co.za'}

        fields = {'LAT': latitude,
                  'LON': longitude,
                  'ADDRESS': address,
                  'GCACCURACY': 'ROOFTOP'}

        result = self.http.request('GET', self.url + self.techapiv2, headers=headers, fields=fields)

        if result.status == 200:
            try:
                data = json.loads(result.data.decode('utf-8'))
                verified = data.get('AddressVerify')[0]
            except json.JSONDecodeError:
                return 400
            else:
                if verified:
                    latitude = verified.get('LR_LAT')
                    longitude = verified.get('LR_LON')
                    address = verified.get('LR_Address')
                    amid = verified.get('AMID')

                    fields = {'LAT': latitude,
                              'LON': longitude,
                              'ADDRESS': address,
                              'AMID': amid,
                              'GCACCURACY': 'VERIFIED'}

                    result = self.http.request('GET', self.url + self.techapiv2, headers=headers, fields=fields)

                    if result.status == 200:
                        try:
                            data = json.loads(result.data.decode('utf-8'))
                        except json.JSONDecodeError:
                            return 400
                        else:
                            if data.get('errorCode') == 0:
                                payload = data.get('results').get('items')[0].get('payload')
                                response = {'id': 0,
                                            'company': 'Openserve',
                                            'logo': 'https://openserve.co.za/open/assets/_images/openserve_logo.svg',
                                            'ftth': 0,
                                            'status': ''}

                                if payload:
                                    ftth = payload.get('FTTHBoundary')
                                    status = payload.get('ftthInfrastructure').get('ftthInfo')[0].get('FTTH_Status')

                                    response['ftth'] = ftth
                                    response['status'] = status

                                    return response
                                else:
                                    return 400
                            else:
                                return 400

        else:
            return result.status
