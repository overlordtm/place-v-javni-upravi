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


    df = pju.fetch.fetch_payouts()

    df.to_csv('data/pju/data/payout_types.csv')

    resource = Resource(path='data/pju/data/payout_types.csv')

    # infer metadata from resource and add it to the package
    resource.infer()


    package = Package()
    package.add_resource(resource)

    package.to_yaml('data/pju/datapackage.yaml')