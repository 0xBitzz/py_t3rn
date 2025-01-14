from __future__ import annotations

from dataclasses import dataclass
from typing import Type, TypeVar

from config import Config
from connection.helpers import connect_to_rpc
from eth_account.signers.local import LocalAccount
from transaction.constants import OPT_ARB_INPUT_DATA, OPTIMISM_NETWORK
from utils.logging import setup_logger

from web3 import AsyncWeb3, Web3
from web3.middleware import SignAndSendRawMiddlewareBuilder

logger = setup_logger(__name__)

T = TypeVar("T", bound="Transaction")


@dataclass(frozen=True, kw_only=True)
class TransactionParams:
    amount: int
    receiver: str
    input_data: str


class Transaction:
    def __init__(self, *, account: LocalAccount, provider: AsyncWeb3) -> None:
        """
        Initializes the Transaction class with the given account and provider.

        Args:
        -----
            config (Config): The configuration object containing necessary settings.
            provider: The provider object for interacting with the blockchain.
        """
        self.account = account
        self.provider = provider
        self.provider.middleware_onion.inject(
            SignAndSendRawMiddlewareBuilder.build(self.account),
            layer=0,
        )

    @classmethod
    async def create(cls: Type[T], config: Config) -> T:
        """
        Asynchronous factory method to create a Transaction instance.

        Args:
        -----
            config (Config): The configuration object containing necessary settings.

        Returns:
        --------
            Transaction: An initialized Transaction instance.
        """
        account = config.account
        provider = await connect_to_rpc(config)
        logger.info("Connected to provider for account: %s", account.address)
        return cls(account=account, provider=provider)

    async def balance_in_wei(self) -> int:
        """
        Retrieves the account balance in wei.

        Returns:
        -------
            int: The account balance in wei.
        """
        balance = await self.provider.eth.get_balance(self.account.address)
        logger.debug("Balance in wei for account %s: %d", self.account.address, balance)
        return balance

    async def balance_in_ether(self) -> float:
        """
        Retrieves the account balance in ether.

        Returns:
        -------
            float: The account balance in ether.
        """
        balance = Web3.from_wei(await self.balance_in_wei(), "ether")
        logger.debug(
            "Balance in ether for account %s: %f", self.account.address, balance
        )
        return balance

    async def process_transaction(self, *, tx_params: TransactionParams) -> str:
        """
        Processes a transaction and returns the transaction URL.

        Returns:
        -------
            str: The URL of the transaction on the blockchain explorer.

        Raises:
        -------
            Exception: If an error occurs during the transaction process.
        """
        logger.info("Starting transaction process...")

        tx_dict = {
            "from": self.account.address,
            "to": tx_params.receiver,
            "value": tx_params.amount,
            "nonce": await self.provider.eth.get_transaction_count(
                self.account.address
            ),
            "chainId": await self.provider.eth.chain_id,
            "data": tx_params.input_data,
        }

        try:
            estimated_gas = await self.provider.eth.estimate_gas(tx_dict) * 1.2
            tx_dict["gas"] = int(estimated_gas)

            txn_hash = await self.provider.eth.send_transaction(tx_dict)
            logger.info("Transaction sent. Hash: 0x%s", txn_hash.hex())

            await self.provider.eth.wait_for_transaction_receipt(txn_hash)
            return txn_hash.hex()

        except Exception as e:
            logger.error("Error processing transaction: %s", e, exc_info=True)
            raise


async def main():
    import os

    import config

    config = config.Config(
        private_key=os.getenv("PRIVATE_KEY"), rpc_url=os.getenv("OPT_SEPOLIA_RPC_URL")
    )
    transaction = await Transaction.create(config=config)
    print(f"Balance in ETH: {await transaction.balance_in_ether()}")
    print(f"Balance in WEI: {await transaction.balance_in_wei()}")
    await transaction.process_transaction(
        receiver=OPTIMISM_NETWORK,
        amount=Web3.to_wei(0.1, "ether"),
        input_data=OPT_ARB_INPUT_DATA,
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
