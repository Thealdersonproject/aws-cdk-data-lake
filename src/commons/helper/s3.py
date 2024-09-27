import aws_cdk as cdk
import re

from typing import Dict, List
from jsii.python import classproperty

from commons.constructs.s3 import S3 as S3Core
from commons.model import Resource, ResourceType
from commons.utils import (
    constants,
    resource_name as resource_utils
)
from commons.utils.loader import Loader


class S3:
    """
    Class to organize S3 bucket creation related functions.
    To interact directly with from commons_cdk_core.storage.s3.S3BucketStack class
    Resource description:
            resource name:          Amazon Simple Storage Service
            resource description:   Amazon Simple Storage Service (Amazon S3) is an object storage service that
                                    offers industry-leading scalability, data availability, security, and performance.
            resource web page:      https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html
            resource name rules:    https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
            resource short name:    s3
            resource type:          storage / object storage
    """

    @staticmethod
    def _resource_name(logical_name: str) -> str:

        if not logical_name:
            raise ValueError("Logical name must be provided.")

        kwargs:Dict[str, str] = {
            "company_short_name": Loader().company.short_name,
            "environment": Loader().account.environment,
            "project_short_name": Loader().project.short_name,
            "resource_short_name": "s3",
            "separator": constants.DEFAULT_RESOURCE_NAME_PATTERN_SEPARATOR,
        }

        resource_name:str = resource_utils.format_logical_name(
            resource_name_allow_upper_case=False,
            resource_name_forbidden_chars=["_"],
            resource_name_forbidden_start=["xn--", "sthree-", "sthree-configurator", "amzn-s3-demo-"],
            resource_name_forbidden_end=["-s3alias", "--ol-s3", ".mrap", "--x-s3"],
            resource_name_min_size=3,
            resource_name_max_size=63,
            resource_name_allow_numeric=True,
            logical_name=logical_name,
            resource_name_separator=constants.DEFAULT_RESOURCE_NAME_PATTERN_SEPARATOR,
            resource_name_forbidden_chars_new_value=constants.DEFAULT_RESOURCE_NAME_PATTERN_SEPARATOR,
            resource_name_pattern=constants.AWS_DEFAULT_RESOURCE_NAME_PATTERN,
            **kwargs
        )

        """
            as per s3 bucket naming rule, it is not allowed to have bucket names with IP Address pattern
            for example: 192.168.5.4
            
            if happens, "." will be replaced for the {separator} 
            this is an S3 bucket naming rule only.
        """
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", resource_name):
            resource_name =  resource_name.replace(
                ".",
                f"{constants.DEFAULT_RESOURCE_NAME_PATTERN_SEPARATOR}"
            )

        return resource_name

    @classproperty
    def s3_bucket_resource_type(self) -> ResourceType:
        """
        Returns an instance of ResourceType configured for Amazon S3.

        The returned ResourceType object contains metadata specific to Amazon Simple Storage Service (S3),
        including resource type, product name, short name, description, resource group, and name pattern separator.

        @returns
            ResourceType: An instance of ResourceType with S3-specific settings.
        """
        return ResourceType(
            product_name="Amazon Simple Storage Service",
            product_description="Amazon Simple Storage Service (Amazon S3) is an object storage service that offers "+\
                                "industry-leading scalability, data availability, security, and performance.",
            product_web_link="https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
            short_name="s3",
            resource_type="OBJECT::STORAGE",
            name_pattern_separator=constants.HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR,
        )

    @staticmethod
    def create_basic_bucket(
        cdk_stack: cdk.Stack,
        bucket_name: str,
        additional_tags: Dict[str, str],
        kms_key: cdk.aws_kms.Key | cdk.aws_kms.IKey | None,
        versioned: bool = False,
    ) -> cdk.aws_s3.Bucket:
        """

        Creates an S3 bucket with the specified configurations.

        Parameters:
        cdk_stack (cdk.Stack): The Cloud Development Kit stack to which the bucket will be added.
        bucket_name (str): The logical name of the bucket to create.
        additional_tags (Dict[str, str]): Additional tags to apply to the bucket.
        kms_key (cdk.aws_kms.Key | cdk.aws_kms.IKey | None): The Key Management Service (KMS) key for bucket encryption, if any.
        versioned (bool): Whether to enable versioning for the bucket. Default is False.

        Returns:
        cdk.aws_s3.Bucket: The created S3 bucket instance.

        """
        s3_bucket_config: Resource = Resource.load_resource(
            logical_name=bucket_name, resource_type=S3.s3_bucket_resource_type
        )

        tags_to_apply = s3_bucket_config.tags | additional_tags
        return S3Core().create_bucket(
            scope=cdk_stack,
            bucket_id=s3_bucket_config.resource_name,
            bucket_name=s3_bucket_config.resource_name,
            tags=tags_to_apply,
            encryption_key=kms_key,
            versioned=versioned,
        )
