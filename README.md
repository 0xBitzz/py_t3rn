# PY_T3RN

## Overview

This project is a Python-based solution for automating transactions using the Web3.py library. It supports asynchronous processing and interacts with Ethereum-based networks via RPC endpoints.

## Disclaimer

This project is not affiliated with, endorsed by, or related to the [original t3rn project](https://www.t3rn.io/). It is an independent implementation of an automated transaction script designed for personal or educational use.

## Features

- Transaction Processing: Automates sending transactions, including setting gas and waiting for transaction receipts.

- Balance Management: Monitors account balance and halts transactions when a specified threshold is reached.

- Asynchronous Operations: Utilizes asyncio for efficient handling of asynchronous tasks.

- Configurable Settings: Stores and manages sensitive configuration details like private keys and RPC URLs securely.

## Dependencies

- Python 3.8+

- web3.py

- asyncio

- python-dotenv

## Setup

1. Clone the Repository
    ```sh
    git clone https://github.com/0xBitzz/py_t3rn.git
    ```
    ```sh
    cd py_t3rn
    ```

2. Install Dependencies

    It is recommended to use a virtual environment:

    ```sh
    python -m venv env
    ```
    ```sh
    source env/bin/activate
    ```
    ```sh
    pip install -r requirements.txt
    ```

3. Configure the Project

    Create a `.env` file and enter your private key and RPC URL (See the [.env.example](.env.example) file for hint):
    ```txt
    PRIVATE_KEY=your_private_key_here
    ```
    ```env
    RPC_URL=https://your_rpc_url_here
    ```

4. Run the Application
    ```py
    python3 py_t3rn
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
