from typing import Literal

import requests
import time
import logger


log = logger.get_logger(__name__)


class RESTAPI:
    auth: tuple = None  # optional parameter to use http authentication
    headers: dict = None  # optional parameters to set http headers

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.elapsed_time = None

    def _request(self,
                 url: str,
                 method: Literal['GET', 'POST', 'PUT', 'DELETE'],
                 payload: object) -> requests.Response:
        """
        Generic method to call requests.Request
        :param url:str URL to send
        :param method:str allowed methods:['GET', 'POST', 'PUT', 'DELETE']
        :param payload:dict will be passed as 'params' for GET and DELETE, as 'data' for PUT and POST requests
        :return:
        """

        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise AttributeError(f'Method {method} is not allowed.')

        request_params = {'params': payload} if method in ['GET', 'DELETE'] else {'data': payload}

        request = requests.Request(url=url, method=method, **request_params, auth=self.auth, headers=self.headers)
        log.debug(f'url: {url}')
        prepped_request = request.prepare()
        session = requests.Session()

        _start = time.time()
        response = session.send(prepped_request, timeout=self.timeout)
        self.elapsed_time = time.time() - _start

        log.debug(f'Status code returned: {response.status_code}')
        session.close()

        # here you can save request execution time to a database to see how requests performance behave in time
        log.debug(f'elapsed time: {self.elapsed_time}')

        try:
            log.debug(f'json result if json exists: {response.json()}')
        except Exception as e:
            log.exception(e)

        return response

    def get(self, url: str, payload=None) -> requests.Response:
        return self._request(url, method='GET', payload=payload)

    def post(self, url: str, payload=None) -> requests.Response:
        return self._request(url, method='POST', payload=payload)

    def put(self, url: str, payload=None) -> requests.Response:
        return self._request(url, method='PUT', payload=payload)

    def delete(self, url: str, payload=None) -> requests.Response:
        return self._request(url, method='DELETE', payload=payload)
