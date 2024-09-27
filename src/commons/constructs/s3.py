from typing import Any, Dict, List

import aws_cdk as cdk


class S3:
    """
    S3 class provides utilities for managing AWS S3 buckets within AWS CDK stacks.

    useful links:
        API Reference aws_cdk.aws_s3 - Bucket: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
        Naming pattern: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
    """

    @staticmethod
    def create_bucket(
        scope: cdk.Stack,
        bucket_id: str | None,
        bucket_name: str,
        tags: Dict[str, str],
        **kwargs: Any,
    ) -> cdk.aws_s3.Bucket:
        """
        Creates an S3 bucket with the specified parameters and returns the bucket object.

        Arguments:
            scope (cdk.Stack): The CDK stack in which the bucket is created.
            bucket_id (str | None): The ID of the bucket. If not provided, the bucket_name will be used as the ID.
            bucket_name (str): The name of the S3 bucket. Must not be empty or blank.
            tags (Dict[str, str]): A dictionary of tags to add to the S3 bucket.
            **kwargs: Additional keyword arguments that are passed to the S3 bucket constructor.

        Returns:
            cdk.aws_s3.Bucket: The created S3 bucket object.

        Raises:
            ValueError: If the bucket_name is empty or blank.
        """
        if not bucket_name or bucket_name.strip():
            raise ValueError("Bucket name cannot be empty")

        if not bucket_id or bucket_id.strip():
            bucket_id = bucket_name

        bucket = cdk.aws_s3.Bucket(
            scope=scope,
            id=bucket_id,
            bucket_name=bucket_name,
            enforce_ssl=True,
            minimum_tls_version=1.2,
            **kwargs,
        )

        # S3 default tags
        cdk.Tags.of(bucket).add(key="resource", value="s3 bucket")

        # Add tags to the S3 bucket
        for key in tags:
            cdk.Tags.of(bucket).add(key=key, value=tags[key])

        return bucket

    @staticmethod
    def apply_permissions(
        bucket: cdk.aws_s3.Bucket,
        permissions: List[Dict[str, cdk.aws_iam.IGrantable]] | List[cdk.aws_iam.IGrantable],
    ) -> None:
        """
        Apply permissions to the specified S3 bucket.

        This method iterates over a list of permissions and applies each permission to the given S3 bucket
        based on the specified action and principal. Permissions can be provided as dictionaries or
        `cdk.aws_iam.IGrantable` objects. Supported actions are 'read', 'write', and 'read_write'.

        Args:
            bucket (cdk.aws_s3.Bucket): The S3 bucket to which permissions will be applied.
            permissions (List[Dict[str, cdk.aws_iam.IGrantable]] | cdk.aws_iam.IGrantable): A list of permissions to be applied. Each permission can be a dictionary
            containing an 'action' and a 'principal', or an instance of `cdk.aws_iam.IGrantable`.
        """
        for permission in permissions:
            if isinstance(permission, dict):
                action = permission.get("action")
                principal = permission.get("principal")
                if action == "read":
                    bucket.grant_read(principal)  # type: ignore
                elif action == "write":
                    bucket.grant_write(principal)  # type: ignore
                elif action == "read_write":
                    bucket.grant_read_write(principal)  # type: ignore
                # Add more actions as needed

            elif isinstance(permission, cdk.aws_iam.IGrantable):  # type: ignore
                bucket.grant_read(permission)

    @staticmethod
    def add_bucket_permission(
        bucket: cdk.aws_s3.Bucket, action: str, principal: cdk.aws_iam.IPrincipal
    ) -> None:
        """
        Adds a specified permission to an AWS S3 bucket for a given principal.

        Args:
            bucket (cdk.aws_s3.Bucket): The S3 bucket to which the permission will be added.
            action (str): The type of permission to be granted. Valid values are 'read', 'write', and 'read_write'.
            principal (cdk.aws_iam.IPrincipal): The principal (e.g., IAM user or role) that will receive the specified permission.

        Raises:
            ValueError: If an unsupported action is provided in the 'action' parameter.
        """
        if action == "read":
            bucket.grant_read(principal)
        elif action == "write":
            bucket.grant_write(principal)
        elif action == "read_write":
            bucket.grant_read_write(principal)
