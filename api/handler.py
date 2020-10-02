import json
import time

import aiohttp

from geocoding import Geocoding
from providers.openserve import OpenServe

openserve = OpenServe()
geocoding = Geocoding()


async def myrequest(session, method, url, params=None, data=None, headers=None):
    async with session.request(method=method, url=url, params=params, data=data, headers=headers) as response:
        return await response.text(), response.status


class MessageHandler:
    async def response_handler(self, data):
        try:
            data = json.loads(data)

            async with aiohttp.ClientSession() as session:
                address, latitude, longitude = await geocoding.geocoding(session, data)

                response = {'event': 'response', 'providers': []}

                response['providers'].append(await openserve.fetch_services(session, address, latitude, longitude))

            time.sleep(0.1)

        except json.JSONDecodeError:
            return {'event': 'error', 'msg': 'invalid json'}
        else:
            return response
