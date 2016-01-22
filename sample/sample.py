#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe 
#
# Distributed under terms of the MIT license.

import requests
from bs4 import BeautifulSoup

def process(url):
    resp = requests.get(url) ##
    body = BeautifulSoup(resp.content)
    title = body.select('title')[0].text
    return title


if __name__ == '__main__':
    print process('http://www.google.com')


