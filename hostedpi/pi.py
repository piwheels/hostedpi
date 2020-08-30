from datetime import datetime, timedelta

import requests


class Pi:
    def __init__(self, parent, name, model):
        self._parent = parent
        self._name = name
        self._model = model
        self._destroyed = False
        self._next_status_check = datetime.now()

    def __repr__(self):
        if self.destroyed:
            return f'<hostedpi.Pi {self.name} destroyed>'
        else:
            return f'<hostedpi.Pi model {self.model} {self.name}>'

    @property
    def name(self):
        return self._name

    @property
    def destroyed(self):
        return self._destroyed

    @property
    def model(self):
        return self._model

    @property
    def cache_is_invalid(self):
        return datetime.now() > self._next_status_check

    @property
    def data(self):
        if self.destroyed:
            raise HostedPiException('Pi is destroyed')
        if self.cache_is_invalid:
            url = f'{self._parent._API_URL}/{self.name}'
            try:
                r = requests.get(url, headers=self._parent._headers)
            except RequestException as e:
                raise HostedPiException(str(e))
            if r.status_code == 200:
                self._data = r.json()
            else:
                raise HostedPiException(f'status code {r.status_code}')
            self._next_status_check = datetime.now() + timedelta(minutes=1)
        return self._data

    @property
    def disk_size(self):
        return self.data['disk_size']

    @property
    def ssh_port(self):
        return self.data['ssh_port']

    @property
    def ip(self):
        return self.data['ip']

    @property
    def ip_routed(self):
        return self.data['ip_routed']

    @property
    def location(self):
        return self.data['location']

    @property
    def status(self):
        return self.data['status']

    @property
    def initialised_keys(self):
        return self.data['initialised_keys']

    @property
    def power(self):
        return self.data['power']

    def reboot(self):
        url = f'{self._parent._API_URL}/{self.name}'
        r = requests.reboot(url, headers=self._parent._headers)
        return r.json()

    def destroy(self):
        url = f'{self._parent._API_URL}/{self.name}'
        r = requests.delete(url, headers=self._parent._headers)
        body = r.json()
        if 'error' in body:
            raise HostedPiException(body['error'])
        else:
            self._destroyed = True
            del self._parent._pis[self.name]
            return body
