import json
import requests

class Client:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def _modify_args(self, args, kwargs):
        args = list(args)
        kwargs = dict(kwargs)

        args[0] = self.base_url + args[0]

        cookies = kwargs.get('cookies', {})
        if self.token:
            cookies.update({'me': self.token})

        kwargs['cookies'] = cookies

        return args, kwargs

    def post(self, *args, **kwargs):

        args, kwargs = self._modify_args(args, kwargs)
        return requests.post(*args, **kwargs)

    def get(self, *args, **kwargs):

        args, kwargs = self._modify_args(args, kwargs)
        return requests.get(*args, **kwargs)

    def login(self, login, passwd):

        r = requests.post(self.base_url + 'login', data={'login': login, 'passwd': passwd})
        self.token = r.history[0].cookies['me']

        return r

    def logout(self):

        if not self.logged_in():
            raise Exception('not logged in')

        r = self.post('logout')
        self.token = None

        return r

    def logged_in(self):
        return self.token is not None
