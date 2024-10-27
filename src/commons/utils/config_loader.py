"""Loads information to be used in different modules."""

import logging

from commons.model import Account, Company, Project, Storage, Tags
from commons.utils import ProcessLogger, singleton, utils


@singleton
class ConfigLoader:
    """Singleton class to configure the project."""

    def __init__(self, configs: dict[str, dict[str, str]]) -> None:
        """Initializes the ConfigLoader object.

        :param configs: A dictionary containing configuration settings required for initializing the ProcessLogger
        and loading various information such as company, project, account, storage, and additional tags.
        The keys should include 'company', 'project', 'account', 'data-lake-storage', and 'additional-tags'.
        """
        # initialize logger. as it is a singleton, this will keep its instance for further process execution.
        self.logger = ProcessLogger(process_name="", log_level=logging.DEBUG)

        additional_tags: dict[str, str] = configs.get("additional-tags", {})
        self.company: Company | None = None
        self.project: Project | None = None
        self.account: Account | None = None
        self.storage: Storage | None = None
        self.tags: Tags | None = None

        self.properties_for_resource_naming: dict[str, str] | None = None

        self._load_company_information(configs.get("company", {}))
        self._load_project_information(configs.get("project", {}))
        self._load_account_information(configs.get("account", {}))
        self._load_storage_information(configs.get("data-lake-storage", {}))
        self._load_tags(additional_tags)
        self._load_properties_for_resource_naming()

    def _load_company_information(self, configs: dict[str, str]) -> None:
        """Loads company information.

        :param configs: A dictionary containing configuration settings to initialize the Company object.
        This dictionary should have keys and values corresponding to the parameters required by the Company class.
        :return: This method does not return any value. It initializes the company attribute with a new
        Company object and logs the company name and short name.
        """
        self.company = Company(**configs)
        self.logger.info("Company: name %s, short-name %s.", self.company.name, self.company.short_name)

    def _load_project_information(self, configs: dict[str, str]) -> None:
        """Loads project information.

        :param configs: A dictionary containing project configuration parameters.
        :return: None
        """
        self.project = Project(**configs)
        self.logger.info("Project: name %s, short-name %s.", self.project.name, self.project.short_name)

    def _load_account_information(self, configs: dict[str, str]) -> None:
        """Loads company information.

        :param configs: A dictionary containing account configuration details.
        It expects keys such as "id", "region", and "environment".
        :return: None
        """
        account_id_key: str = configs["id"]
        account_id: str = utils.get_env(key=account_id_key)

        account_region_key: str = configs["region"]
        account_region: str = utils.get_env(key=account_region_key)

        account_environment_key: str = configs["environment"]
        account_environment: str = utils.get_env(key=account_environment_key)

        self.account = Account(id=account_id, region=account_region, environment=account_environment)
        self.logger.info(
            "Account: id %s, region %s, environment %s.",
            self.account.id,
            self.account.region,
            self.account.environment
        )

    def _load_storage_information(self, configs: dict[str, str]) -> None:
        """Loads storage information.

        :param configs: Configuration dictionary containing storage settings.
        :return: None
        """
        self.storage = Storage(**configs)
        self.logger.info("Storage Information")
        self.logger.info(" :: First layer :: >> %s.", self.storage.first_layer)
        self.logger.info(" :: Second layer :: >> %s.", self.storage.second_layer)
        self.logger.info(" :: Third layer :: >> %s.", self.storage.third_layer)
        self.logger.info(" :: Landing-zone :: >> %s.", self.storage.landing_zone)
        self.logger.info(" :: Assets folder :: >> %s.", self.storage.assets)

    def _load_tags(self, additional_tags: dict[str, str] | None) -> None:
        """Loads tags information.

        :param additional_tags: Dictionary containing additional tags to be loaded.
        :return: None
        """
        self.tags = Tags(
            company=self.company,
            project=self.project,
            account=self.account,
            additional_tags=additional_tags,
        )
        if self.tags.default:
            self.logger.info("Tags Information")
            for tag, value in self.tags.default.items():
                self.logger.info("::%s:: >> %s", tag, value)

    def _load_properties_for_resource_naming(self) -> None:
        """Populates the properties_for_resource_naming attribute with company, project, and account-related data.

        :return: None
        """
        self.properties_for_resource_naming = {
            "company-name": self.company.name,
            "company-short_name": self.company.name,
            "project-name": self.project.name,
            "project-short_name": self.project.name,
            "account-id": self.account.id,
            "account-region": self.account.region,
            "account-environment": self.account.environment,
        }
        self.logger.info("Properties for resource naming:")
        for key, value in self.properties_for_resource_naming.items():
            self.logger.info("::%s:: >> %s", key, value)
