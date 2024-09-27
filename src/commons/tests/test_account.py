import unittest

from commons.model.account import Account


class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        """
        This code contains a setup method that initializes an Account object for testing purposes.

        Parameters:
        - id: The ID of the account.
        - region: The region of the account.
        - environment: The environment of the account.

        Example usage:
        account_test_object = Account(id="test_id", region="test_region", environment="test_environment")
        """
        self.account_test_object = Account(
            id="test_id", region="test_region", environment="test_environment"
        )

    def test_account_init(self) -> None:
        """
        This code defines a test case method `test_account_init` for the `Account` class.

        The code uses the `self.assertEqual()` method to perform assertions on the attributes of an instance of the `Account` class (`self.account_test_object`).

        - The first assertion checks if the `id` attribute of the `Account` instance is initialized with the value `"test_id"`. If the assertion fails, an error message of "Account ID did not initialize correctly" is displayed.

        - The second assertion checks if the `region` attribute of the `Account` instance is initialized with the value `"test_region"`. If the assertion fails, an error message of "Account region did not initialize correctly" is displayed.

        - The third assertion checks if the `environment` attribute of the `Account` instance is initialized with the value `"test_environment"`. If the assertion fails, an error message of "Account environment did not initialize correctly" is displayed.

        These assertions are used to verify that the initialization of the `Account` instance is working correctly.

        The purpose of this code is to test the initialization of the `Account` class and ensure that the attributes are correctly set during the initialization process.
        """
        self.assertEqual(
            self.account_test_object.id,
            "test_id",
            "Account ID did not initialize correctly",
        )
        self.assertEqual(
            self.account_test_object.region,
            "test_region",
            "Account region did not initialize correctly",
        )
        self.assertEqual(
            self.account_test_object.environment,
            "test_environment",
            "Account environment did not initialize correctly",
        )

    def test_account_id(self) -> None:
        """
        This is a test method that verifies the functionality of changing the account ID value for an account object.

        The test involves setting a new ID value for the account object and then asserting that the ID value has indeed been changed correctly.

        The test validates the correctness of the account ID value change functionality.

        Parameters:
            - self: the instance of the test class that this method belongs to

        Returns:
            - None

        """
        self.account_test_object.id = "new_id"
        self.assertEqual(
            self.account_test_object.id,
            "new_id",
            "Account ID value did not change correctly",
        )

    def test_account_region(self) -> None:
        """
        This function is used to test the region value of an account.

        Parameters:
            - self (object): The object of the test class.

        Returns:
            None

        Example:
            test_object = TestClass()
            test_object.test_account_region()
        """
        self.account_test_object.region = "new_region"
        self.assertEqual(
            self.account_test_object.region,
            "new_region",
            "Account region value did not change correctly",
        )

    def test_account_environment(self) -> None:
        """
        This function is used to test the environment property of an account object.

        Parameters:
        - self: The instance of the test class.

        Returns:
        - None

        Raises:
        - AssertionError: If the environment value did not change correctly.

        Example usage:
        test = TestClass()
        test.test_account_environment()
        """
        self.account_test_object.environment = "new_environment"
        self.assertEqual(
            self.account_test_object.environment,
            "new_environment",
            "Account environment value did not change correctly",
        )
