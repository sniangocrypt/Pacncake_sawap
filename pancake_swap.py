import asyncio
import time

from client import Client
from config import PANCAKE_CONTRACTS, PANCAKE_ROUTER_ABI, PANCAKE_QUOTER_ABI, TOKENS_PER_CHAIN, ZERO_ADDRESS,ERC20_ABI

value = 0.001
SLIPPAGE = 1

FULL = True # OR False - ЕСЛИ КОНКРЕТУНЮ СУММУ СВОПАЕТЕ or True - ЕСЛИ ХОТИТЕ СВАПНУТЬ ВЕСЬ БАЛАНС


class Pancake:
    def __init__(self, client: Client):
        self.client = client
        self.quoter_contract = self.client.get_contract(
            contract_address=PANCAKE_CONTRACTS[self.client.chain_name]['quoter'],
            abi=PANCAKE_QUOTER_ABI
        )
        self.router_contract = self.client.get_contract(
            contract_address=PANCAKE_CONTRACTS[self.client.chain_name]['router'],
            abi=PANCAKE_ROUTER_ABI
        )

    def get_path(self, from_token_name: str, to_token_name: str):
            pool_fee: int = {
                "Arbitrum": {
                    'ETH/USDC.e': 500,
                    'USDC.e/ETH': 500,
                    f"{from_token_name}/{to_token_name}": 500
                }
            }[self.client.chain_name][f"{from_token_name}/{to_token_name}"]

            from_address_bytes = self.client.w3.to_bytes(
                hexstr=TOKENS_PER_CHAIN[self.client.chain_name][from_token_name])
            to_address_bytes = self.client.w3.to_bytes(hexstr=TOKENS_PER_CHAIN[self.client.chain_name][to_token_name])
            pool_fee_bytes = pool_fee.to_bytes(3, 'big')

            return from_address_bytes + pool_fee_bytes + to_address_bytes

    async def get_min_amount_out(self, path: str, amount_in_wei: int):
            min_amount_out = await self.quoter_contract.functions.quoteExactInput(
                path,
                amount_in_wei
            ).call()

            return int(min_amount_out[0] * (1 - SLIPPAGE / 100))

    async def swap(self, from_token_name: str, to_token_name: str, amount: float, full: bool):

            if FULL == False:  # СВАП ДЛЯ КОНКРЕТНОГО КОЛИЧЕСТВА ТОКЕНОВ
                decimals = await self.client.get_decimals(token_name=from_token_name)
                amount_in_wei = self.client.to_wei_custom(amount, decimals)
                path = self.get_path(from_token_name, to_token_name)

                deadline = int(time.time() + 1200)
                min_amount_out_in_wei = await self.get_min_amount_out(path, amount_in_wei)
                value = amount_in_wei if from_token_name == self.client.chain_token else 0

                if from_token_name != self.client.chain_token:
                    from_token_address = TOKENS_PER_CHAIN[self.client.chain_name][from_token_name]
                    await self.client.make_approve(
                        token_address=from_token_address, spender_address=self.router_contract.address,
                        amount_in_wei=amount_in_wei
                    )

                full_data = [self.router_contract.encodeABI(
                    fn_name='exactInput',
                    args=([
                        [
                            path,
                            self.client.address if to_token_name != self.client.chain_token else ZERO_ADDRESS,
                            deadline,
                            amount_in_wei,
                            min_amount_out_in_wei
                        ]
                    ])
                )]

                if from_token_name == self.client.chain_token or to_token_name == self.client.chain_token:
                    additional_data = self.router_contract.encodeABI(
                        fn_name='refundETH' if from_token_name == 'ETH' else 'unwrapWETH9',
                        args=() if from_token_name == 'ETH' else (
                            min_amount_out_in_wei,
                            self.client.address
                        )
                    )
                    full_data.append(additional_data)

                transaction = await self.router_contract.functions.multicall(
                    full_data
                ).build_transaction(await self.client.prepare_tx(value=value))

                return await self.client.send_transaction(transaction, without_gas=True)

            if FULL == True:  # СВАП ДЛЯ ВСЕГО КОЛИЧЕСТВА ТОКЕНОВ НА БАЛАНСЕ

                self.erc20 = self.client.get_contract(
                    contract_address=TOKENS_PER_CHAIN[self.client.chain_name][from_token_name],
                    abi=ERC20_ABI
                )
                amount_full = await self.erc20.functions.balanceOf(self.client.address).call()
                path = self.get_path(from_token_name, to_token_name)
                deadline = int(time.time() + 1200)
                min_amount_out_in_wei = await self.get_min_amount_out(path, amount_full)
                value = amount_full if from_token_name == self.client.chain_token else 0

                if from_token_name != self.client.chain_token:
                    from_token_address = TOKENS_PER_CHAIN[self.client.chain_name][from_token_name]
                    await self.client.make_approve(
                        token_address=from_token_address, spender_address=self.router_contract.address,
                        amount_in_wei=amount_full
                    )

                full_data = [self.router_contract.encodeABI(
                    fn_name='exactInput',
                    args=([
                        [
                            path,
                            self.client.address if to_token_name != self.client.chain_token else ZERO_ADDRESS,
                            deadline,
                            amount_full,
                            min_amount_out_in_wei
                        ]
                    ])
                )]

                if from_token_name == self.client.chain_token or to_token_name == self.client.chain_token:
                    additional_data = self.router_contract.encodeABI(
                        fn_name='refundETH' if from_token_name == 'ETH' else 'unwrapWETH9',
                        args=() if from_token_name == 'ETH' else (
                            min_amount_out_in_wei,
                            self.client.address
                        )
                    )
                    full_data.append(additional_data)

                transaction = await self.router_contract.functions.multicall(
                    full_data
                ).build_transaction(await self.client.prepare_tx(value=value))

                return await self.client.send_transaction(transaction, without_gas=True)


private_key = ''
proxy = ''

w3_client = Client(private_key=private_key, proxy=proxy)
swap_client = Pancake(client=w3_client)

asyncio.run(swap_client.swap('USDC', 'ETH', value, FULL))

