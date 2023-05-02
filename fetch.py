#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pju.package

def fetch_and_package():
    pju.package.package_data(year=2021)
    pju.package.package_data(year=2022)
    

if __name__ == '__main__':
    fetch_and_package()