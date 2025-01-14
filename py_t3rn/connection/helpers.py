from typing import Optional

from config import Config
from utils.logging import setup_logger

from web3 import AsyncBaseProvider, AsyncHTTPProvider, AsyncWeb3

logger = setup_logger(__name__)

async def connect_to_rpc(config: Config) -> Optional[AsyncWeb3]:
    """
    Establish a connection to the RPC provider.

    Args:
    -----
        config (Config): The configuration object containing the RPC URL.

    Returns:
    --------
        Optional[AsyncWeb3]: An instance of AsyncWeb3 if the connection is successful, otherwise None.

    Raises:
    -------
        Exception: If there is an error during the connection attempt.
    """
    logger.info("Connecting to RPC provider...")
    provider = AsyncWeb3(AsyncHTTPProvider(config.rpc_url))
    if await is_connected(provider):
        logger.info("Successfully connected to RPC provider.")
        return provider
    else:
        logger.error("Failed to connect to RPC provider.")
        raise ConnectionError("RPC connection failed.")


async def disconnect_from_rpc(provider: AsyncBaseProvider) -> None:
    """
    Disconnects the connection to the RPC provider by closing all active sessions.

    Args:
    -----
        provider (AsyncBaseProvider): The RPC provider to disconnect from.

    Raises:
    -------
        Exception: If an error occurs during the disconnection process, it will be logged.
    """
    try:
        if provider:
            for (
                _,
                session,
            ) in provider.provider._request_session_manager.session_cache.items():
                logger.info("Disconnecting from RPC provider...")
                await session.close()
    except Exception as e:
        logger.error(f"Error during disconnection: {e}")


async def is_connected(provider: AsyncBaseProvider) -> bool:
    """
    Check if the provider is connected.

    Args:
    -----
        provider (AsyncBaseProvider): The provider to check the connection status for.

    Returns:
    -------
        bool: True if the provider is connected, False otherwise.
    """
    return await provider.is_connected()
