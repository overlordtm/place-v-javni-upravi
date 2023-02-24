#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pju
import datetime
import os
from frictionless import Package, Resource
from datapackage_to_datasette import datapackage_to_datasette, DataImportError

def fetch_and_package():
    os.chdir('data/pju')
    today = datetime.date.today()

    metadata = {
        'name': 'pju',
        'title': 'Salaries in Slovenian public sector',
        'description': 'This datapackage contains salaries in Slovenian public sector since 2010',
        'version': f'{today.year}.{today.month}.{today.day}',
    }
    package = Package(**metadata)

    df = pju.fetch_payouts()
    df.to_csv('data/by_type.csv')
    res = Resource(path='data/by_type.csv', name='by_type')
    res.infer()
    res.schema.primary_key = ['year_month']
    package.add_resource(res)

    df = pju.fetch_payouts_by_budget_user_group(2020, 1)
    df.to_csv('data/by_budget_user_group.csv')
    res = Resource(path='data/by_budget_user_group.csv', name='by_budget_user_group')
    res.infer()
    res.schema.primary_key = ['year_month', 'group_id']
    package.add_resource(res)

    df = pju.fetch_payouts_by_budget_user(2020, 1)
    df.to_csv('data/by_budget_user.csv')
    res = Resource(path='data/by_budget_user.csv', name='by_budget_user')
    res.infer()
    res.schema.primary_key = ['year_month', 'budget_user_id', 'budget_user_name']
    package.add_resource(res)

    df = pju.fetch_payouts_by_job_title(2020, 1)
    df.to_csv('data/by_job_title.csv')
    res = Resource(path='data/by_job_title.csv', name='by_job_title')
    res.infer()
    res.schema.fields[res.schema.field_names.index('group_id')].type = 'string'
    res.schema.primary_key = ['year_month', 'job_title_id', 'budget_user_id', 'budget_user_name']
    package.add_resource(res)

    package.to_yaml('datapackage.yaml')

    os.chdir('../..')
    os.makedirs('ds', exist_ok=True)
    datapackage_to_datasette(
        'ds/pju.db',
        'data/pju/datapackage.yaml',
        'metadata.json',
        write_mode='replace'
    )

if __name__ == '__main__':
    fetch_and_package()