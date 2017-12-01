import c
import requests


def get(url,headers):
    return requests.get(c.site + url, verify=False, headers=headers)


def put(url,headers,data):
    return requests.put(c.site + url,verify=False, headers=headers,
                 data=data)


def post(url,headers,data):
    return requests.post(c.site + url,verify=False, headers=headers,
                 data=data)