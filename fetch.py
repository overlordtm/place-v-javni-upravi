#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pju.package

def fetch_and_package():
    pju.package.package_data(year=2021)
    

if __name__ == '__main__':
    fetch_and_package()