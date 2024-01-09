import pytest

from dj_rest_auth_saml.utils import decode_relay_state
from dj_rest_auth_saml.utils import string_to_int_hash


@pytest.mark.UTILS
def test_decode_relay_state():

    ret = decode_relay_state(None)
    assert isinstance(ret, dict)
    assert not ret

    ret = decode_relay_state("")
    assert isinstance(ret, dict)
    assert not ret

    url = "http://www.example.com?param1=value1&param2=value2"
    expected = {"next": url}
    ret = decode_relay_state(url)
    assert isinstance(ret, dict)
    assert ret == expected

    relative_path = "/relative/path?param1=value1&param2=value2"
    ret = decode_relay_state(relative_path)
    expected = {"next": relative_path}
    assert isinstance(ret, dict)
    assert ret == expected

    params = "param1=value1&param2=value2"
    expected = {"param1": "value1", "param2": "value2"}
    ret = decode_relay_state(params)
    assert isinstance(ret, dict)
    assert ret == expected


@pytest.mark.UTILS
def test_string_to_int_hash():
    s = ""
    result = string_to_int_hash(s)
    assert isinstance(result, int)
    assert result == 281949768489412648962353822266799178366
