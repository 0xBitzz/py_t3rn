import os

from eth_account.signers.local import LocalAccount
from web3 import Account


class ConfigMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Config:
    """
    Config class for storing configuration settings.
    """
    def __init__(self, *, private_key: str, rpc_url: str) -> None:
        """
        Args:
        -----
            private_key (str): The private key required for signing transactions.
            rpc_url (str): The RPC URL.
        """
        assert private_key, "Private key is required"
        assert rpc_url, "RPC URL is required"

        self.__private_key = private_key
        self.__rpc_url = rpc_url

    @property
    def account(self) -> LocalAccount:
        """
        Retrieves the local account associated with the stored private key.

        Returns:
        -------
            LocalAccount: The local account object derived from the private key.
        """
        return Account.from_key(self.__private_key)

    @property
    def private_key(self) -> str:
        """
        Returns:
        -------
            str: Returns a masked version of the private key.
        """
        masked = f"{self.__private_key[:4]}{'*' * (len(self.__private_key) - 8)}{self.__private_key[-4:]}"
        return masked

    @property
    def rpc_url(self) -> str:
        """
        Returns the RPC URL.

        Returns:
        -------
            str: Returns the RPC URL.
        """
        return self.__rpc_url

    @private_key.setter
    def private_key(self, value: str):
        """
        Prevent setting the private key after initialization.

        Raises:
        -------
            AttributeError: If there's an attempt to set the private key after initialization.
        """
        raise AttributeError("Private key cannot be modified after initialization.")

    @rpc_url.setter
    def rpc_url(self, value: str):
        """
        Prevent setting the RPC URL after initialization.

        Raises:
        -------
            AttributeError: If there's an attempt to set the RPC URL after initialization.
        """
        raise AttributeError("RPC URL cannot be modified after initialization.")


if __name__ == "__main__":
    config = Config(private_key=os.getenv("PRIVATE_KEY"), rpc_url="OPT_SEPOLIA_RPC_URL")
    print(config.private_key)
    print(config.account)
    print(config.rpc_url)
