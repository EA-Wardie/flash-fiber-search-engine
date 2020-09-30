import urllib3
import json

http = urllib3.PoolManager()


class Vumatel:
    def __init__(self):
        self.url = 'https://cdn.vumatel.co.za/mapdata/'
        self.filenames = ['master_village.json', 'master_reach.json', 'master_core.json']
        self.mapdata = list()
        self.endpoint = None

    def download_mapdata(self):
        for file in self.filenames:
            result = http.request('GET', self.url + file)

            if result.status != 200:
                return 'Download Failed'
            else:
                self.mapdata.append(json.loads(result.data))

        return 'Download Completed'

    # async def fetch_results(self, lat, long, address):
    #     request = f'LAT={lat}&LON={long}&ADDRESS={address}&GCACCURACY=VERIFIED'
    #
    #     async with aiohttp.ClientSession as session:
    #         async with session.get(self.url + self.endpoint + request) as response:
    #             print(response.status)
    #             print(await response.text())
    #             print(response.content)
