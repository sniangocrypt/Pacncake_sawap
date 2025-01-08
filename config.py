import json

WETH_ADDRESS = '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1'
HYPERLANE_NFT_ADDRESS = '0x7daC480d20f322D2ef108A59A465CCb5749371c4'

Orbiter_router = {
    'Arbitrum': "0x6a065083886EC63d274b8E1fE19aE2ddF498bFDd"
}

ZRO_ClAIM_ADDRESS = {
    'Arbitrum': "0xB09F16F625B363875e39ADa56C03682088471523"
}

CLAIM_CONTRACT = {'Arbitrum': "0x060e7c1bc320C9e7C1760e06A5455c343D16603B"
}

STARGATE_DST_ID = {
    'Arbitrum': 30110,
    'Optimism': 30111
}

STARGATE_CONTRACTS = {
    'Arbitrum': {
        'router_eth': "0xA45B5130f36CDcA45667738e2a258AB09f4A5f7F",
        'router_eth_fast': "0xbf22f0f184bCcbeA268dF387a49fF5238dD23E40"
    },
    'Optimism': {
        'router_eth': "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3",
        'router_eth_fast': "0xe8CDF27AcD73a434D661C84887215F7598e7d0d3"
    }
}

AAVE_CONTRACTS = {
    'Arbitrum': {
        'native': "0xecD4bd3121F9FD604ffaC631bF6d41ec12f1fafb",
        'pool': "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
        'aArbWETH': "0xe50fA9b3c56FfB159cB0FCA61F5c9D750e8128c8"
    }
}

SYNCSWAP_CONTRACTS = {
    'zkSync': {
        'pool_factory': '0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb',
        'paymaster': '0x0c08f298A75A090DC4C0BB4CaA4204B8B9D156c1',
        'router_v2': '0x9B5def958d0f3b6955cBEa4D5B7809b2fb26b059'
    }
}

UNISWAP_CONTRACTS = {
    'Arbitrum': {
        'quoter': '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6',
        'router': '0xE592427A0AEce92De3Edee1F18E0157C05861564'
    }
}

PANCAKE_CONTRACTS = {
    'Arbitrum': {
        'quoter': '0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997',
        'router': '0x1b81D678ffb9C0263b24A97847620C99d213eB14'
    }
}


ETH_MASK = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

TOKENS_PER_CHAIN = {
    'Arbitrum': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "USDC.e": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "ZRO": "0x6985884C4392D348587B19cb9eAAf157F13271cd",
    },
    'Optimism': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
    },
    'Ethereum': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    },
    'zkSync': {
        "ETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "WETH": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        "USDT": "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
        "USDC.e": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4"
    }
}

Multicoll = {
    'Arbitrum': "0xcA11bde05977b3631167028862bE2a173976CA11",
    'Ethereum': "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696",
    'Optimism': "0x5e227AD1969Ea493B43F840cff78d08a6fc17796"
}

CHAIN_ID_BY_NAME = {
    'Arbitrum': 42161,
    'Optimism': 10,
    'Ethereum': 1
}

with open('abis/abi.json') as file:
    ERC20_ABI = json.load(file)

with open('abis/weth_abi.json') as file:
    WETH_ABI = json.load(file)


with open('abis/stargate.json') as file:
    STARGATE_ROUTER_ABI = json.load(file)

with open('abis/stargate_fast.json') as file:
    STARGATE_ROUTER_FAST_ABI = json.load(file)

with open('abis/claim.json') as file:
    CLAIM = json.load(file)

with open('abis/orbiter_arb.json') as file:
    Orbiter_arb = json.load(file)

with open('abis/multicoll.json') as file:
    Multicol_json = json.load(file)

with open('abis/uniswap.json') as file:
    UNISWAP_ROUTER_ABI = json.load(file)

with open('abis/uniswap_qouter.json') as file:
    UNISWAP_QUOTER_ABI = json.load(file)

with open('abis/pancake.json') as file:
    PANCAKE_ROUTER_ABI = json.load(file)

with open('abis/pancake_qouter.json') as file:
    PANCAKE_QUOTER_ABI = json.load(file)
