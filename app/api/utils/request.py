import os
import json
import requests


class Request(object):
    def __init__(self, base, api=None):
        self.base = base
        self.api = api
        self.path = None
        self.data = None
        self.method = None
        self.res = None

        # headers
        self.headers = dict()

        if self.method != "delete":
            self.headers['Content-Type'] = "application/json"

    def send(self, verify=True):

        if self.api:
            self.path = os.path.join(self.base, self.api)
        else:
            self.path = self.base

        if self.data:
            self.data = json.dumps(self.data)

        if self.method == "put":
            request_fn = requests.put
        elif self.method == "get":
            request_fn = requests.get
        elif self.method == "patch":
            request_fn = requests.patch
        elif self.method == "delete":
            request_fn = requests.delete
        else:
            request_fn = requests.post

        try:
            self.res = request_fn(
                self.path, headers=self.headers, data=self.data, timeout=60)
        except requests.ConnectionError as e:
            return Exception(str(e))
        except Exception as e:
            raise Exception(str(e))

        response = json.loads(self.res.content)
        if not 200 <= self.res.status_code < 300:
            raise Exception
        else:
            return response


class RavePayment(Request):
    def __init__(self):
        url = os.getenv("FLUTTERWAVE_API_URL")
        super(RavePayment, self).__init__(base=url)

    def pay(self, payload):
        self.method = 'post'
        self.api = 'payments'
        self.headers['Authorization'] = f'Bearer {os.getenv("FLUTTERWAVE_SECRET_KEY")}'
        self.data = payload
        response = dict()
        try:
            response = super(RavePayment, self).send()
        except Exception:
            raise Exception
        return response

    def verify(self, transaction_id=None):
        self.method = 'get'
        self.api = f'transactions/{transaction_id}/verify'
        self.headers['Authorization'] = f'Bearer {os.getenv("FLUTTERWAVE_SECRET_KEY")}'
        response = dict()
        try:
            response = super(RavePayment, self).send()
        except Exception as e:
            raise Exception(str(e))
        return response
