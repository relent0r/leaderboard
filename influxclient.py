import logging
import json
import requests
import requests.exceptions

logger = logging.getLogger(__name__)

class influxclient(object):
    """
    Some client functions for v2 alpha of influxdb. Uses tokens for auth. Assuming influxdb container with http
    """

    def __init__(self, host, port, org, token, bucket):
        self.host = host
        self.port = port
        self.token = token
        self.org = org
        self.bucket = bucket
        self.scheme = "http"
        self.path = "/api/v2/"
        self.url = "{0}://{1}:{2}{3}".format(
            self.scheme,
            self.host,
            self.port,
            self.path)
        self.headers = {
            'Content-Type': 'text/plain',
            'Accept': 'text/plain',
            'Authorization': 'Token ' + token
        }
    
    def write(self, data):
        headers = self.headers
        uri = self.url + 'write'
        org = self.org
        bucket = self.bucket
        querystring = {"org":org, "bucket":bucket, "precision":"ms"}
        try:
            response = requests.request("POST", uri, headers=headers, params=querystring, data=data)
            if response.status_code != 204:
                response.raise_for_status() 
            elif response.status_code == 204:
                data = response.status_code
                logger.debug(data)
        except requests.exceptions.HTTPError:
            logger.warning('request error, response code is %s', response.status_code)

    