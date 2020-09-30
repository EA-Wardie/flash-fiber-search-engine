import json


class OpenServe:
    def __init__(self):
        self.url = 'https://gis.telkom.co.za'
        self.endpoint = '/apps/api/ucmTechAPIV'

    # async def fetch_results(self, lat, long, address):
    #     request = f'LAT={lat}&LON={long}&ADDRESS={address}&GCACCURACY=VERIFIED'
    #
    #     async with aiohttp.ClientSession() as session:
    #         response = await session.get(self.url + self.endpoint + request)
    #
    #         print(response.status)
    #         print(await response.text())
    #         print(response.content)