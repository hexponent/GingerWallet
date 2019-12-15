from bitcoinlib.wallets import HDWallet, wallet_delete
import bitcoinlib.transactions
import bitcoinlib.encoding
import hashlib
from bitcoinlib.mnemonic import Mnemonic
import codecs
import base58check


passphrase = "space cricket train sell disagree assume onion soap journey style camera false"
wallet_name = "trial"

#w = HDWallet.create(wallet_name, keys=passphrase, network='testnet', db_uri='./trial.db')
w = HDWallet(wallet_name, db_uri='./trial.db')
#w.utxos_update()
key = w.get_key()

address = key.address
print("address:", address)
# TODO: hash160 not working
# print("hash", bitcoinlib.encoding.hash160(address))
print(w.balance())

tx_hash = w.utxos()[-1]['tx_hash']

t = w.transaction(tx_hash)
script = t.outputs[0].lock_script
print(t.outputs[0].script_type)
# print(codecs.decode(t.outputs[0].lock_script, 'base58'))
print(script)

print(bitcoinlib.transactions.script_to_string(script))

