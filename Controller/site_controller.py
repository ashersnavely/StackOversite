import requests
# noinspection PyProtectedMember
from bs4 import BeautifulSoup, Tag

from Controller.site_constants import *
from Objects.site import Site


class SiteController:
    _site_controller = None

    @staticmethod
    def get_instance():
        if not SiteController._site_controller:
            SiteController._site_controller = _SiteController(SiteController.__fetch_site_options(),
                                                              SiteController.__fetch_method_options())

        return SiteController._site_controller

    @staticmethod
    def __fetch_site_options():
        response = requests.get(f'{api_url}/{api_version}/sites').json()
        return [item['site_url'].replace('https://', '').replace('.com', '') for item in response['items']]

    @staticmethod
    def __fetch_method_options():
        api_soup = BeautifulSoup(requests.get(f'{api_url}/docs').content, 'html.parser')
        method_options = {}

        for method in Methods:
            sub_methods = api_soup.find('body').find('a', text=f'{method.value}').parent.parent.parent.contents
            sub_methods = [item for item in sub_methods if isinstance(item, Tag)]

            options = []
            for sub_method in sub_methods:
                method_description = sub_method.find('div', {'class': 'method-description'}).text.strip()
                if 'auth required' not in method_description:
                    method_name = sub_method.find('div', {'class': 'method-name'}).text.strip()

                    options.append({'method_name': method_name,
                                    'method_description': method_description,
                                    'id_required': '{id' in method_name})

            method_options.update({method: options})

        return method_options


class _SiteController:
    def __init__(self, site_options: list, method_options: list):
        self.site_options = site_options
        self.method_options = method_options
        self.sites = {}

    def create_site(self, url: str, **kwargs):
        if url in self.site_options:
            if url not in self.sites:
                self.sites.update({url: Site(url, **kwargs)})
                return True
            return False

    def delete_site(self, url: str):
        self.sites.pop(url)

    def get_site(self, url: str):
        return self.sites[url]
