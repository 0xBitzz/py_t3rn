import asyncio
import os

from config import Config
from connection.helpers import disconnect_from_rpc
from transaction.constants import OPT_ARB_INPUT_DATA, OPTIMISM_NETWORK
from transaction.transaction import Transaction, TransactionParams
from utils.logging import setup_logger

from web3 import Web3

logger = setup_logger(__name__)

WELCOME_TEXT = r"""
 /$$$$$$$  /$$     /$$ /$$$$$$$$ /$$$$$$  /$$$$$$$  /$$   /$$
| $$__  $$|  $$   /$$/|__  $$__//$$__  $$| $$__  $$| $$$ | $$
| $$  \ $$ \  $$ /$$/    | $$  |__/  \ $$| $$  \ $$| $$$$| $$
| $$$$$$$/  \  $$$$/     | $$     /$$$$$/| $$$$$$$/| $$ $$ $$
| $$____/    \  $$/      | $$    |___  $$| $$__  $$| $$  $$$$
| $$          | $$       | $$   /$$  \ $$| $$  \ $$| $$\  $$$
| $$          | $$       | $$  |  $$$$$$/| $$  | $$| $$ \  $$
|__/          |__/       |__/   \______/ |__/  |__/|__/  \__/
"""

BALANCE_THRESHOLD = 0.1
SLEEP_DURATION = 30


async def main():
    private_key = os.getenv("PRIVATE_KEY")
    rpc_url = os.getenv("OPT_SEPOLIA_RPC_URL")

    if not private_key or not rpc_url:
        logger.error(
            "Environment variables PRIVATE_KEY and OPT_SEPOLIA_RPC_URL are required."
        )
        return

    config = Config(private_key=private_key, rpc_url=rpc_url)
    logger.info("Configuration loaded.")

    transaction = await Transaction.create(config=config)
    balance = await transaction.balance_in_ether()
    logger.info("Account balance before the transaction: %.4f ETH", balance)

    try:
        while True:
            if balance <= BALANCE_THRESHOLD:
                logger.warning("Insufficient balance for the transaction.")
                await disconnect_from_rpc(transaction.provider)
                break

            txn_hash = await transaction.process_transaction(
                tx_params=TransactionParams(
                    receiver=OPTIMISM_NETWORK,
                    amount=Web3.to_wei(0.1, "ether"),
                    input_data=OPT_ARB_INPUT_DATA,
                )
            )

            explorer_url = f"https://sepolia-optimistic.etherscan.io/tx/0x{txn_hash}."
            logger.info("Transaction URL: %s", explorer_url)
            balance = await transaction.balance_in_ether()
            logger.info("Account balance after the transaction: %.4f ETH", balance)

            for i in range(SLEEP_DURATION, 0, -1):
                print(
                    f"\rSleeping for {i} second(s) before initiating another transaction.",
                    end="",
                    flush=True,
                )
                await asyncio.sleep(1)
            logger.info("\nSleep complete.\nStarting the next transaction.\n")

    except Exception as e:
        await disconnect_from_rpc(transaction.provider)
        print(e)
        return


def run():
    logger.info("%s", WELCOME_TEXT)
    asyncio.run(main())


if __name__ == "__main__":
    run()
