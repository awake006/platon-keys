from eth_utils import (
    keccak,
)
from platon_keys.utils.bech32 import to_wit, encode

HRP = "plt"


def public_key_bytes_to_address(public_key_bytes: bytes) -> bytes:
    return keccak(public_key_bytes)[-20:]


def compressed_public_key_bytes_to_address(compressed_public_key_bytes: bytes) -> str:
    witver, witprog = to_wit(compressed_public_key_bytes)
    return encode(HRP, witver, witprog)
