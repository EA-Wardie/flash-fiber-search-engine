from providers import openserve
from providers import vumatel


class ProviderLookup:
    def __init__(self):
        self.providers = list()

        self.providers.append('openserve')
        self.providers.append(openserve.OpenServe())

        self.providers.append('vumatel')
        self.providers.append(vumatel.Vumatel())

    def get_providers(self, provider: str):
        try:
            index = self.providers.index(provider)
            return self.providers[index + 1]
        except ValueError:
            return None

    def get_url(self, provider: str):
        return self.get_providers(provider).url

    def get_endpoint(self, provider: str):
        return self.get_providers(provider).endpoint
