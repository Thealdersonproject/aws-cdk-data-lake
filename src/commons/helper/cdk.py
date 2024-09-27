import aws_cdk as cdk
from jsii.python import classproperty

from commons.model.resource import Resource
from commons.model.resource_type import ResourceType
from commons.utils import constants
from commons.utils.loader import Loader


class CommonCdk:

    @classproperty
    def cdk_stack_resource_type(self) -> ResourceType:
        return ResourceType(
            product_name="AWS::CloudFormation::Stack",
            product_description="Stack is a collection of one or more constructs.",
            product_web_link="https://docs.aws.amazon.com/cdk/v2/guide/stacks.html",
            short_name="stack",
            resource_type="CDK::IAC",
            name_pattern_separator=constants.HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR,
        )

    @staticmethod
    def create_cdk_stack(
        app: cdk.App, stack_name: str, stack_description: str | None = None
    ) -> cdk.Stack:
        if not app:
            raise ValueError("app must be provided")

        if not stack_name or not isinstance(stack_name, str) or not stack_name.strip():
            raise ValueError("stack_name must be a non-empty string")

        if not stack_description:
            stack_description = stack_name

        loader: Loader = Loader()
        stack_resource_type: ResourceType = CommonCdk.cdk_stack_resource_type
        stack: Resource = Resource.load_resource(
            logical_name=stack_name, resource_type=stack_resource_type
        )

        cdk_env = cdk.Environment(account=loader.account.id, region=loader.account.region)
        cdk_stack = cdk.Stack(
            scope=app,
            id=stack.resource_name,
            description=stack_description,
            tags=stack.tags,
            env=cdk_env,
        )

        return cdk_stack
