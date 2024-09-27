# mypy: ignore-errors
import os
from pathlib import Path
from typing import Dict, List, Any

import toml
from dotenv import load_dotenv

from commons.utils import constants
from commons.utils.common_decorators import singleton

load_dotenv()


@singleton
class Loader:
    """
    Loader class for loading and managing configurations related to company information, data lake storage, environment variables, projects, and resource naming patterns.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        Raises:
            ValueError: If no configuration is provided or if the configuration values are empty.

        """
        # Account information
        self._account: Dict[str, str] | None = None

        # Sets each data lake layer names
        self._first_layer_name: str | None = None
        self._second_layer_name: str | None = None
        self._third_layer_name: str | None = None
        self._landing_zone_name: str | None = None
        self._assets_name: str | None = None

        # Default resource name pattern
        self.default_name_pattern: str | None = None

        # Default tags
        self.default_tags: Dict[str, str] | None = None

        # All other information loaded from config file
        self.config_information: Dict[str, Dict[str, str]] | None = None

        self.load_config_file()

    def load_config_file(self) -> None:
        # values expected to exist on config file:
        config_file_root_account = "account"
        account_environment = "environment"
        account_id = "id"
        account_region = "region"

        config_file_root_data_lake_storage = "data_lake_storage"
        data_lake_storage_assets = "data_lake_assets"
        data_lake_storage_landing_zone = "landing_zone_name"
        data_lake_storage_first_layer = "first_layer_name"
        data_lake_storage_second_layer = "second_layer_name"
        data_lake_storage_third_layer = "third_layer_name"

        config_file = Loader._find_config_file()
        with open(config_file, "r", encoding=constants.DEFAULT_ENCODING) as f:
            config: Dict[str, Dict[str, Any]] = toml.load(f)

        if not config or not config.values():
            raise ValueError("No configuration was provided.")

        if config_file_root_account not in config.keys() or not {
            account_environment,
            account_id,
            account_region
        }.issubset(config[config_file_root_account].keys()):
            raise ValueError("Account information is expected to be informed.")

        # validate and load data lake layer name pattern
        if config_file_root_data_lake_storage not in config.keys() or not {
            data_lake_storage_assets,
            data_lake_storage_landing_zone,
            data_lake_storage_first_layer,
            data_lake_storage_second_layer,
            data_lake_storage_third_layer
        }.issubset(config[config_file_root_data_lake_storage].keys()):
            raise ValueError("Data Lake layer names are expected to be informed.")
        else:
            storage_config_content = config[config_file_root_data_lake_storage]
            self._assets_name = storage_config_content[data_lake_storage_assets]
            self._landing_zone_name = storage_config_content[data_lake_storage_landing_zone]
            self._first_layer_name = storage_config_content[data_lake_storage_first_layer]
            self._second_layer_name = storage_config_content[data_lake_storage_second_layer]
            self._third_layer_name = storage_config_content[data_lake_storage_third_layer]

            config.pop(config_file_root_data_lake_storage)

    @property
    def first_layer_name(self) -> str | None:
        return self._first_layer_name

    @property
    def second_layer_name(self) -> str | None:
        return self._second_layer_name

    @property
    def third_layer_name(self) -> str | None:
        return self._third_layer_name

    @property
    def landing_zone_name(self) -> str | None:
        return self._landing_zone_name

    @property
    def assets_name(self) -> str | None:
        return self._assets_name

    @staticmethod
    def _find_config_file(filename: str = "config.toml", max_depth: int = 5) -> str:
        """
        A static method that finds a configuration file in the current working directory or its parent directories.

        :param filename: The name of the configuration file to search for. The default value is "config.toml".
        :type filename: str
        :param max_depth: The maximum number of parent directories to search. The default value is 5.
        :type max_depth: int
        :return: The full path of the configuration file if found, or an empty string if not found.
        :rtype: str
        """
        current_dir = Path.cwd()
        for _ in range(max_depth):
            config_path = current_dir / filename
            if config_path.is_file():
                return str(config_path.resolve())  # Return full path as string, including filename
            if current_dir.parent == current_dir:
                # We've reached the root of the filesystem
                break
            current_dir = current_dir.parent
        return ""

    @staticmethod
    def _get_env_variable(var_name: str, default: str = "-1") -> str:
        """
            Retrieves the value of the environment variable with the specified name.

            If the environment variable is not set, returns the provided default value.

            Args:
                var_name (str): The name of the environment variable to look up.
                default (str): The value to return if the environment variable is not found. Defaults to "-1".

            Returns:
                str: The value of the environment variable, or the default value if not set.
        """
        return os.getenv(var_name, default)
