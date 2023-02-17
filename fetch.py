#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pju
from frictionless import Package, Resource

def fetch_and_package():
    package = Package()

    df = pju.fetch_payouts()
    df.to_csv('data/pju/data/by_type.csv')
    package.add_resource(Resource(path='data/pju/data/by_type.csv'))

    df = pju.fetch_payout_by_budget_user_group(2020, 1)
    df.to_csv('data/pju/data/by_budget_user_group.csv')
    package.add_resource(Resource(path='data/pju/data/by_budget_user_group.csv'))

    df = pju.fetch_payout_by_budget_user(2020, 1)
    df.to_csv('data/pju/data/by_budget_user.csv')
    package.add_resource(Resource(path='data/pju/data/by_budget_user.csv'))

    df = pju.fetch_payouts_job_title(2020, 1)
    df.to_csv('data/pju/data/by_job_title.csv')
    package.add_resource(Resource(path='data/pju/data/by_job_title.csv'))

    package.to_yaml('data/pju/datapackage.yaml')
    

if __name__ == '__main__':
    fetch_and_package()