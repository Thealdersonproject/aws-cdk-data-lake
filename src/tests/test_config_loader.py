import pytest

from commons.utils import ConfigLoader


@pytest.fixture
def configloader_instance():
    configs = {
        "account": {
            "id": "ACCOUNT_ID",
            "region": "REGION_ID",
            "environment": "ENVIRONMENT_NAME"
        },
        "data-lake-storage": {
            "first_layer": "raw",
            "second_layer": "stage",
            "third_layer": "analytics",
            "landing_zone": "landing",
            "assets": "data-lake-assets",
        },
        "company": {
            "name": "Amazon Web Services",
            "short_name": "aws"
        },
        "project": {
            "name": "Data Lakehouse",
            "short_name": "dlh"
        },
        "additional-tags": {
            "tag": "Me"
        },
    }
    cl = ConfigLoader(configs)
    return cl


def test_properties_for_resource_naming(configloader_instance):
    properties = configloader_instance.properties_for_resource_naming
    assert properties["company-name"] == "Amazon Web Services"
