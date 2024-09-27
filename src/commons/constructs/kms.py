from typing import Any, Dict

from aws_cdk import RemovalPolicy, Stack, Tags
from aws_cdk import aws_kms as kms


class KMS:
    """
    KMS class provides utilities for managing AWS KMS Keys within AWS CDK stacks.

    useful links:
        API Reference aws_cdk.aws_s3 - Bucket: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_kms/Key.html
    """

    @staticmethod
    def create_kms_key(
        scope: Stack,
        kms_id: str,
        description: str | None,
        alias: str | None = None,
        enabled: bool = True,
        enable_key_rotation: bool = True,
        removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
        tags: Dict[str, str] | None = None,
        **kwargs: Any,
    ) -> kms.Key:
        """

            Create an AWS KMS key with the specified properties.

            @param scope: The AWS CDK stack in which this resource is defined.
            @param kms_id: A unique identifier for the KMS key.
            @param description: A description for the KMS key. If not provided, defaults to kms_id.
            @param alias: An alias for the KMS key. If not provided, defaults to kms_id.
            @param enabled: Specifies whether the key is enabled. Default is True.
            @param enable_key_rotation: Specifies whether key rotation is enabled. Default is True.
            @param removal_policy: The removal policy for the key. Default is RemovalPolicy.RETAIN.
            @param tags: A dictionary of tags to associate with the KMS key.
            @param kwargs: Additional keyword arguments to pass to the KMS key resource.
            @returns: An instance of kms.Key representing the created KMS key.
            @raises ValueError: If kms_id is empty or None.

        """
        if not kms_id or not kms_id.strip():
            raise ValueError("kms_id cannot be empty")

        if not alias or not alias.strip():
            alias = kms_id

        if not description or not description.strip():
            description = kms_id

        if not alias.startswith("alias/"):
            alias = f"alias/{alias}"

        kms_key = kms.Key(
            scope,
            id=kms_id,
            alias=alias,
            description=description,
            enabled=enabled,
            enable_key_rotation=enable_key_rotation,
            removal_policy=removal_policy,
            **kwargs,
        )

        # kms default tags
        Tags.of(kms_key).add(key="resource", value="kms key")

        # Add tags to the KMS object
        if tags:
            for key in tags:
                Tags.of(kms_key).add(key=key, value=tags[key])

        return kms_key
