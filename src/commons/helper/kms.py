from typing import Any

import aws_cdk as cdk
from jsii.python import classproperty

from commons.constructs.kms import KMS
from commons.model.resource import Resource
from commons.model.resource_type import ResourceType
from commons.utils import constants


class Kms:

    @classproperty
    def kms_resource_type(self) -> ResourceType:
        return ResourceType(
            product_name="AWS Key Management Service",
            product_description="AWS Key Management Service (AWS KMS) is a managed service that makes it easy for "+\
                                "you to create and control the cryptographic keys that are used to protect your data.",
            product_web_link="https://docs.aws.amazon.com/kms/latest/developerguide/overview.html",
            short_name="kms",
            resource_type="SECURITY::CRYPTOGRAPHY",
            name_pattern_separator=constants.HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR,
        )

    @staticmethod
    def create_kms_key(
        stack: cdk.Stack,
        key_id: str,
        description: str,
        alias: str,
        tags: dict,
        enabled: bool = True,
        enable_key_rotation: bool = True,
        removal_policy: cdk.RemovalPolicy = cdk.RemovalPolicy.RETAIN,
        **kwargs: Any,
    ) -> cdk.aws_kms.Key | cdk.aws_kms.IKey | None:

        kms_config: Resource = Resource.load_resource(
            logical_name=key_id, resource_type=Kms.kms_resource_type
        )

        if not description or not description.strip():
            kms_description = kms_config.resource_type.description
        else:
            kms_description = description

        if not alias or not alias.strip():
            alias = key_id

        kms_key = KMS.create_kms_key(
            scope=stack,
            kms_id=kms_config.resource_name,
            description=kms_description,
            alias=alias,
            enabled=enabled,
            enable_key_rotation=enable_key_rotation,
            removal_policy=removal_policy,
            tags=tags,
            **kwargs,
        )

        return kms_key
