from hypothesis import (
    strategies as st,
)

from eth_utils import (
    int_to_big_endian,
)

from platon_keys.constants import (
    SECPK1_N,
)
from platon_keys.utils.padding import (
    pad32,
)


private_key_st = st.integers(min_value=1, max_value=SECPK1_N).map(
    int_to_big_endian,
).map(pad32)


message_hash_st = st.binary(min_size=32, max_size=32)
signature_st = st.binary(min_size=65, max_size=65)
