import asyncio
import json
from web3 import AsyncWeb3, WebsocketProviderV2


# Настройки WebSocket и адрес пула Uniswap
ALCHEMY_API_URL = "wss://eth-mainnet.g.alchemy.com/v2/URI-jUQPongWWe6_2mMAjn-qW11VHMSR"
POOL_ADDRESS = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"  # Пример: USDC/ETH пул

pool1 = []
#price1 = []
pool2 = []
#price2 = []

# Загружаем ABI пула Uniswap из файла
with open("abi.json") as file:
    POOL_ABI = json.load(file)

# Обработчик событий
def process_event(event, event_type):
    # Определяем тип события и выводим важные данные
    event_args = event["args"]

    if event_type == "Swap":
        print(
            #f"[Swap] Отправитель: {event_args['sender']}, Получатель: {event_args['recipient']}, "
            #f"Сумма0: {event_args['amount0']/ 10**6}, Сумма1: {event_args['amount1']/ 10**18}"
            #f"ЦЕНА: {(event_args['amount0'] / 10 ** 6)/(event_args['amount1'] / 10 ** 18)}"
        )

        price_now = (event_args['amount0'] / 10 ** 6)/(event_args['amount1'] / 10 ** 18)
        price1 = []
        price2 = []
        price1.append(price_now)
        if price1 != price_now:
            price2.append(price_now)
            print(price1)
            print()
            print(price2[0]/price1[0])
            if price2[0]/price1[0] > 1.000099:
                print(f"НОВАЯ ЦЕНА {price2}")
        #print(f"[Unknown Event] {event_type}: {event_args}")


async def monitor_uniswap_pool(POOL_ADDRESS):

    async with AsyncWeb3.persistent_websocket(WebsocketProviderV2(ALCHEMY_API_URL)) as w3:


        pool_contract = w3.eth.contract(address=POOL_ADDRESS, abi=POOL_ABI)

        print("Начинается мониторинг пула Uniswap...\n")

        try:
            while True:
                # Получаем логи для каждого типа событий
                latest_block = await w3.eth.block_number

                # События Swap
                swap_logs = await pool_contract.events.Swap.get_logs(fromBlock=latest_block - 10, toBlock="latest")
                for log in swap_logs:
                    process_event(log, "Swap")

                # Задержка перед следующим запросом
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            print("Мониторинг остановлен.")

        except Exception as e:
            print(f"Ошибка во время мониторинга: {e}")

# Запуск asyncio-цикла
if __name__ == "__main__":
    try:
        asyncio.run(monitor_uniswap_pool(POOL_ADDRESS))
    except Exception as e:
        print(f"Ошибка запуска: {e}")
