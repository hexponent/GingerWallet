import bitcoinlib
import requests


URL = "https://wasabiwallet.io/api/v3/btc/ChaumianCoinJoin"


def get_round_id():
    body = requests.get(URL + "/states")
    return body[0]["roundId"]


def get_inputs(wallet, round_id):
    inputs = {
        "roundId": round_id,
        "inputs": [
            {
                "input": {
                    "transactionId": "30cba70a29a78ccf97a50c23a2c7a3cace6385d866a5ab0105a16aea8508cb15"  #
                },
                "proof": "string"
            }
        ],
        "blindedOutputScripts": [
            {}
        ],
        "changeOutputAddress": {
            "scriptPubKey": {
                "hash": {},
                "witHash": {}
            },
            "network": {
                "consensus": {
                    "buriedDeployments": {},
                    "biP9Deployments": {},
                    "subsidyHalvingInterval": 0,
                    "consensusFactory": {},
                    "majorityEnforceBlockUpgrade": 0,
                    "majorityRejectBlockOutdated": 0,
                    "majorityWindow": 0,
                    "biP34Hash": {},
                    "powLimit": {},
                    "powTargetTimespan": "string",
                    "powTargetSpacing": "string",
                    "powAllowMinDifficultyBlocks": True,
                    "powNoRetargeting": True,
                    "hashGenesisBlock": {},
                    "minimumChainWork": {},
                    "minerConfirmationWindow": 0,
                    "ruleChangeActivationThreshold": 0,
                    "coinbaseMaturity": 0,
                    "coinType": 0,
                    "litecoinWorkCalculation": True,
                    "supportSegwit": True
                },
                "networkType": 0,
                "networkSet": {},
                "genesisHash": {}
            }
        }
    }
    return inputs


def get_wallet(wallet_name, passphrase, db_uri=None, network=None):
    if bitcoinlib.wallets.wallet_exists(wallet_name, db_uri=db_uri):
        return bitcoinlib.wallets.HDWallet(wallet_name, db_uri=db_uri)
    else:
        return bitcoinlib.wallets.HDWallet.create(wallet_name, keys=passphrase, witness_type='segwit',
                                                  network=network, db_uri=db_uri)


def print_wallet_info(w):
    key = w.get_key()
    key_private = key.key_private
    address = key.address
    print("passphrase:", passphrase)
    print("balance:", w.balance())
    print("key_private:", key_private)
    print("address:", address)
    # print(w.info())
    # print(w.utxos())
    print()


if __name__ == "__main__":
    network = "testnet"
    db_uri = "./db"
    # passphrase = bitcoinlib.mnemonic.Mnemonic().generate()
    # wallet_name = "segwit_p2wpkh_receiver"  # receiver
    # passphrase = "marble hidden icon total funny valid test word south thrive uncover six"  # receiver
    wallet_name = "segwit_p2wpkh"  # main
    passphrase = "gorilla evidence into pony energy stage property camera kick before brand spare"  # main

    print(bitcoinlib.wallets.wallets_list(db_uri=db_uri))

    w = get_wallet(wallet_name, passphrase, db_uri=db_uri, network=network)
    # w.utxos_update()

    # WALLET INFO
    print_wallet_info(w)
    exit()

    # SENDING
    amount = 1000
    rec_address = "tb1qpzpc89uwnwak5k2tsctws69cn8ajgnm4cgd0x9"
    transaction = w.send_to(rec_address, amount, network=network, offline=True)
    from pprint import pprint
    pprint(transaction.as_dict())
    # print(transaction.as_dict()["inputs"][0]["prev_hash"])
    exit()

    round_id = get_round_id()
    get_inputs(w, round_id)

    """
    inp_transaction = w.utxos()[0]
    inp = bitcoinlib.transactions.Input(
        inp_transaction["tx_hash"],
        inp_transaction["output_n"],
        # keys=keys,
        network=network
    )
    amount = 1000
    rec_address = "tb1qpzpc89uwnwak5k2tsctws69cn8ajgnm4cgd0x9"
    out = bitcoinlib.transactions.Output(
        amount,
        address=rec_address,
        network=network
    )
    transaction = bitcoinlib.transactions.HDTransaction(
        hdwallet=w,
        inputs=[inp],
        outputs=[out],
        network=network
    )
    keys = w.keys()
    print(transaction.verify())
    transaction.sign(keys=keys)
    print(transaction.verify())
    # print(transaction.as_dict())
    exit()
    """
