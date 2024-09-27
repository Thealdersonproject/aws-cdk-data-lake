import aws_cdk as cdk

from commons.helper.s3 import S3
from commons.utils.common_decorators import singleton
from commons.utils.loader import Loader


@singleton
class DataLakeStorage:
    """
    The DataLakeStorage class manages the creation and access of various S3 Buckets representing different layers in a data lake.
    It utilizes AWS CDK (Cloud Development Kit) for infrastructure as code.

    Attributes:
        cdk_stack (cdk.Stack): The AWS CDK stack where the resources will be created.
        kms_key (cdk.aws_kms.Key | cdk.aws_kms.IKey): The KMS key for encrypting the S3 buckets.
        loader (Loader): The Loader instance responsible for retrieving logical layer names.
        _first_layer_storage (cdk.aws_s3.Bucket | None): S3 bucket for the first layer of the data lake.
        _second_layer_storage (cdk.aws_s3.Bucket | None): S3 bucket for the second layer of the data lake.
        _third_layer_storage (cdk.aws_s3.Bucket | None): S3 bucket for the third layer of the data lake.
        _landing_zone_storage (cdk.aws_s3.Bucket | None): S3 bucket for the landing zone.
        _assets_storage (cdk.aws_s3.Bucket | None): S3 bucket for the assets storage.

    Methods:
        __init__(self, stack, kms_key): Initializes the DataLakeStorage instance, validates the stack and kms_key, and triggers the creation of data lake storage.
        _create_data_lake_storage(): Private method to create S3 buckets for various data lake layers based on names retrieved from the Loader instance.
        _create_data_lake_bucket(layer_logical_name): Private method to create an S3 bucket with the provided logical name and associated KMS key.

    Properties:
        first_layer_storage (cdk.aws_s3.Bucket | None): Gets the S3 bucket for the first layer.
        second_layer_storage (cdk.aws_s3.Bucket | None): Gets the S3 bucket for the second layer.
        third_layer_storage (cdk.aws_s3.Bucket | None): Gets the S3 bucket for the third layer.
        landing_zone_storage (cdk.aws_s3.Bucket | None): Gets the S3 bucket for the landing zone.
        assets_storage (cdk.aws_s3.Bucket | None): Gets the S3 bucket for the assets storage.
    """

    def __init__(self, stack: cdk.Stack, kms_key: cdk.aws_kms.Key | cdk.aws_kms.IKey) -> None:
        if not stack or not isinstance(stack, cdk.Stack):
            raise ValueError("Invalid stack")

        # if passes the validation, creates instance object
        self.cdk_stack: cdk.Stack = stack

        if not kms_key or not isinstance(kms_key, (cdk.aws_kms.Key, cdk.aws_kms.IKey)):  # type: ignore
            raise ValueError("Invalid kms_key")

        # sets given KMS key
        self.kms_key: cdk.aws_kms.Key | cdk.aws_kms.IKey = kms_key

        # creates the loader instance
        self.loader: Loader = Loader()

        # creates the data lake layers buckets
        self._create_data_lake_storage()

    def _create_data_lake_storage(self) -> None:
        """
        Creates and initializes the data lake storage buckets.

        This private method sets up multiple layers of data lake storage by creating S3 buckets
        for each layer based on the logical names provided by the loader. The layers include
        first layer, second layer, third layer, landing zone, and assets storage. If the loader
        does not provide a name for any layer, that particular storage layer is set to None.
        """
        self._first_layer_storage: cdk.aws_s3.Bucket | None = (
            self._create_data_lake_bucket(layer_logical_name=self.loader.first_layer_name)
            if self.loader.first_layer_name
            else None
        )

        self._second_layer_storage: cdk.aws_s3.Bucket | None = (
            self._create_data_lake_bucket(layer_logical_name=self.loader.second_layer_name)
            if self.loader.second_layer_name
            else None
        )

        self._third_layer_storage: cdk.aws_s3.Bucket | None = (
            self._create_data_lake_bucket(layer_logical_name=self.loader.third_layer_name)
            if self.loader.third_layer_name
            else None
        )

        self._landing_zone_storage: cdk.aws_s3.Bucket | None = (
            self._create_data_lake_bucket(layer_logical_name=self.loader.landing_zone_name)
            if self.loader.landing_zone_name
            else None
        )

        self._assets_storage: cdk.aws_s3.Bucket | None = (
            self._create_data_lake_bucket(layer_logical_name=self.loader.assets_name)
            if self.loader.assets_name
            else None
        )

    def _create_data_lake_bucket(self, layer_logical_name: str) -> cdk.aws_s3.Bucket:
        """

        Creates an S3 bucket for the data lake.

        Parameters:
        layer_logical_name (str): The logical name representing the specific data lake layer for which the bucket is being created.

        Returns:
        cdk.aws_s3.Bucket: The created S3 bucket resource.
        """
        return S3.create_basic_bucket(
            cdk_stack=self.cdk_stack,
            bucket_name=layer_logical_name,
            kms_key=self.kms_key,
            additional_tags={"data-lake-bucket": layer_logical_name},
        )

    @property
    def first_layer_storage(self) -> cdk.aws_s3.Bucket | None:
        return self._first_layer_storage

    @property
    def second_layer_storage(self) -> cdk.aws_s3.Bucket | None:
        return self._second_layer_storage

    @property
    def third_layer_storage(self) -> cdk.aws_s3.Bucket | None:
        return self._third_layer_storage

    @property
    def landing_zone_storage(self) -> cdk.aws_s3.Bucket | None:
        return self._landing_zone_storage

    @property
    def assets_storage(self) -> cdk.aws_s3.Bucket | None:
        return self._assets_storage
