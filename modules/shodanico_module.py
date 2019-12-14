#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import mmh3
import shodan
import base64
import requests
from util.config import *
from util.header import Header

class Shodanico:
    def __init__(self, url):
        self.api_key = shodan_key
        self.url = url

    # 请求favicon.ico转换为hash
    def get_hash(self):
        url = self.url + "/favicon.ico" if '://' in self.url else 'http://' + self.url + "/favicon.ico"
        print(url)

        try:
            r = requests.get(url, verify=False, timeout=20, headers=Header.headers)
            if r.headers['Content-Type'] == "image/x-icon":
                favicon = r.content.encode('base64')
                hash = mmh3.hash(favicon)
            else:
                hash = None
        except Exception as e:
            print("[x] Network is error")
            hash = None

        return hash


    # http.favicon.hash查询
    def search(self, hash):
        api = shodan.Shodan(self.api_key)
        try:
            if hash:
                query = "http.favicon.hash:{}".format(hash)
                count = api.count(query)['total']
                if count == 0:
                    print("[-] No result")
                else:
                    print("[+] Get {} ip".format(count))
                    for h in api.search_cursor(query):
                        print("[+] " + h['ip_str'] + ':' + str(h['port']))
            else:
                print("[x] No favicon")
        except Exception as e:
            print(e)
        except KeyboardInterrupt, e:
            exit(1)

