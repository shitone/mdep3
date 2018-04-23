#!/usr/bin/env python
#coding=utf8

import httplib, urllib

httpClient = None
try:
    #params = urllib.urlencode([{"headers":{"h1":"v1","h2":"v2"},"body":"hello body"}])
    params = '[{"body":"hello body3"}]'
    #headers = {"Content-type": "application/x-www-form-urlencoded"
    #                , "Accept": "text/plain"}
    # httpClient = httplib.HTTPConnection("10.116.89.55", 80, timeout=30)
    httpClient = httplib.HTTPConnection("10.116.8.240", 8888, timeout=30)
    httpClient.request("POST", "/", params)

    response = httpClient.getresponse()
    print response.status
    print response.reason
    print response.read()
    print response.getheaders() #获取头信息
except Exception, e:
    print e
finally:
    if httpClient:
        httpClient.close()



