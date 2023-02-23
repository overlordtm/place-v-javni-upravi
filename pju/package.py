import pju.fetch
from frictionless import Package, Resource


def package_data(year: int, month: int = None):
    metadata = {
        "name": "example-data-package",
        "title": "Example Data Package",
        "resources": [
            {
                "name": "example-resource",
                "path": "data.csv",
                "schema": {
                    "fields": [
                        {"name": "id", "type": "integer"},
                        {"name": "name", "type": "string"},
                        {"name": "age", "type": "integer"},
                    ]
                },
            }
        ],
    }
    package = Package()

    df = pju.fetch.fetch_payouts()
    df.to_csv('data/pju/data/by_type.csv')
    package.add_resource(Resource(path='data/pju/data/by_type.csv'))

    df = pju.fetch.fetch_payout_by_budget_user_group(2020, 1)
    df.to_csv('data/pju/data/by_budget_user_group.csv')
    package.add_resource(Resource(path='data/pju/data/by_budget_user_group.csv'))

    df = pju.fetch.fetch_payout_by_budget_user(2020, 1)
    df.to_csv('data/pju/data/by_budget_user.csv')
    package.add_resource(Resource(path='data/pju/data/by_budget_user.csv'))

    df = pju.fetch.fetch_payouts_job_title(2020, 1)
    df.to_csv('data/pju/data/by_job_title.csv')
    package.add_resource(Resource(path='data/pju/data/by_job_title.csv'))

    package.to_yaml('data/pju/datapackage.yaml')