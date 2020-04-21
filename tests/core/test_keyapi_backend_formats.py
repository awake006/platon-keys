import pytest

from platon_keys import KeyAPI
from platon_keys.backends import NativeECCBackend


@pytest.fixture(autouse=True)
def native_backend_env_var(monkeypatch):
    monkeypatch.setenv('ECC_BACKEND_CLASS', 'platon_keys.backends.native.NativeECCBackend')


@pytest.mark.parametrize(
    'backend',
    (
        None,
        NativeECCBackend(),
        NativeECCBackend,
        'platon_keys.backends.NativeECCBackend',
        'platon_keys.backends.native.NativeECCBackend',
    ),
)
def test_supported_backend_formats(backend):
    keys = KeyAPI(backend=backend)
    assert isinstance(keys.backend, NativeECCBackend)
