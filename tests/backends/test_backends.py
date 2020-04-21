import os

import pytest

from hypothesis import (
    given,
)

from platon_keys import KeyAPI
from platon_keys.backends import CoinCurveECCBackend
from platon_keys.backends import NativeECCBackend
from platon_keys.constants import (
    SECPK1_N,
)
from platon_keys.utils.numeric import (
    coerce_low_s,
)

from eth_utils import (
    keccak,
)

from strategies import (
    private_key_st,
    message_hash_st,
)


MSG = b'message'
MSGHASH = keccak(MSG)


backends = [
    NativeECCBackend(),
]

try:
    import coincurve
    backends.append(CoinCurveECCBackend())
except ImportError:
    if 'REQUIRE_COINCURVE' in os.environ:
        raise


def backend_id_fn(backend):
    return type(backend).__name__


@pytest.fixture(params=backends, ids=backend_id_fn)
def key_api(request):
    return KeyAPI(backend=request.param)


def test_ecdsa_sign(key_api, key_fixture):
    private_key = key_api.PrivateKey(key_fixture['privkey'])
    signature = key_api.ecdsa_sign(MSGHASH, private_key)

    assert key_api.ecdsa_verify(MSGHASH, signature, private_key.public_key)


def test_ecdsa_sign_non_recoverable(key_api, key_fixture):
    private_key = key_api.PrivateKey(key_fixture['privkey'])
    signature = key_api.ecdsa_sign_non_recoverable(MSGHASH, private_key)
    non_recoverable_signature = key_api.ecdsa_sign_non_recoverable(MSGHASH, private_key)
    assert non_recoverable_signature.r == signature.r
    assert non_recoverable_signature.s == signature.s

    assert key_api.ecdsa_verify(MSGHASH, signature, private_key.public_key)


def test_ecdsa_verify(key_api, key_fixture):
    signature = key_api.Signature(vrs=key_fixture['raw_sig'])
    public_key = key_api.PublicKey(key_fixture['pubkey'])

    assert key_api.ecdsa_verify(MSGHASH, signature, public_key)


def test_ecdsa_recover(key_api, key_fixture):
    signature = key_api.Signature(vrs=key_fixture['raw_sig'])
    public_key = key_api.PublicKey(key_fixture['pubkey'])

    assert key_api.ecdsa_recover(MSGHASH, signature) == public_key


def test_decompress_public_key_bytes(key_api, key_fixture):
    compressed = key_fixture['compressed_pubkey']
    uncompressed = key_fixture['pubkey']

    key_from_compressed = key_api.PublicKey.from_compressed_bytes(compressed)
    assert key_from_compressed.to_bytes() == uncompressed


def test_compress_public_key_bytes(key_api, key_fixture):
    uncompressed = key_fixture['pubkey']
    compressed = key_fixture['compressed_pubkey']

    key_from_uncompressed = key_api.PublicKey(uncompressed)
    assert key_from_uncompressed.to_compressed_bytes() == compressed


@given(
    private_key_bytes=private_key_st,
)
def test_compress_decompress_inversion(key_api, private_key_bytes):
    private_key = key_api.PrivateKey(private_key_bytes)

    original = private_key.public_key
    compressed_bytes = original.to_compressed_bytes()
    decompressed = key_api.PublicKey.from_compressed_bytes(compressed_bytes)
    assert decompressed == original


@given(
    private_key_bytes=private_key_st,
    message_hash=message_hash_st,
)
def test_signatures_with_high_s(key_api, private_key_bytes, message_hash):
    private_key = key_api.PrivateKey(private_key_bytes)
    low_s_signature = private_key.sign_msg_hash(message_hash)
    assert coerce_low_s(low_s_signature.s) == low_s_signature.s
    high_s = -low_s_signature.s % SECPK1_N
    assert coerce_low_s(high_s) == low_s_signature.s
    high_s_signature = key_api.Signature(vrs=(low_s_signature.v, low_s_signature.r, high_s))
    assert key_api.ecdsa_verify(message_hash, high_s_signature, private_key.public_key)
