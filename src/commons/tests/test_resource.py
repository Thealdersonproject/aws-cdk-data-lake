import unittest

from commons.model.resource import Resource
from commons.model.resource_type import ResourceType
from commons.utils.loader import Loader


class TestResource(unittest.TestCase):

    def setUp(self) -> None:
        loader_config = {
            "data_lake_storage": {
                "first_layer_name": "bronze",
                "second+layer_name": "silver",
                "third_layer_name": "gold",
                "landing_zone_name": "raw",
            },
            "company_information": {
                "name": "Company X",
                "short_name": "XCO",
                "team": "MasterTeam",
            },
            "project": {
                "name": "project XYZ data lake",
                "short_name": "dl",
            },
            "environment_variables": {
                "account_id": "account_id",
                "account_region": "account_region",
                "account_environment": "account_environment",
            },
            "additional_tags": {"project-id": "123-Xyz"},
        }
        loader = Loader(config=loader_config)
        loader.account.region = "us-east-1"
        loader.account.id = "abc123"
        loader.account.environment = "test"
        self.loader = loader

    def test_resource_init(self) -> None:
        resource_type = ResourceType(
            resource_type="MyTest::ResourceType",
            product_name="My test resource product name",
            short_name="mt",
            description="Test resource type",
            resource_group="general-tests",
            name_pattern_separator="-",
        )

        logical_name = "test resource"
        resource_name_pattern = "{environment_variables_environment}{separator}{company_information_short_name}{separator}{project_short_name}{separator}{resource_short_name}{separator}{resource_logical_name}"
        resource = Resource(
            resource_type=resource_type,
            logical_name=logical_name,
            resource_name_pattern=resource_name_pattern,
            resource_name_pattern_separator=resource_type.name_pattern_separator,
        )
        self.assertEqual(resource.resource_name, "test-xco-dl-mt-test_resource")
