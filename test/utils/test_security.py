import pytest
from utils.security import Security

security = Security()


def test_encrypt_decrypt_valid_string():
    """The function encrypts a valid string using a valid key"""
    key = "secret_key"
    value = "Hello, World!"
    security.initialize(key)
    encrypted_value = security.encrypt(value)
    decrypted_value = security.decrypt(encrypted_value)
    assert decrypted_value == value


def test_decrypt_encrypted_string_with_valid_key():
    """The function decrypts an encrypted string using a valid key."""
    key = "secret_key"
    value = "Hello, World!"
    security.initialize(key)
    encrypted_value = security.encrypt(value)
    decrypted_value = security.decrypt(encrypted_value)
    assert decrypted_value != encrypted_value


def test_return_original_string_after_encrypting_and_decrypting():
    """The function returns the original string after encrypting and decrypting."""
    key = "secret_key"
    value = "Hello, World!"
    security.initialize(key)
    encrypted_value = security.encrypt(value)
    decrypted_value = security.decrypt(encrypted_value)
    assert decrypted_value == value


def test_raise_value_error_if_key_is_empty_string():
    """The function raises a ValueError if the key is an empty string."""
    key = ""
    value = "Hello, World!"
    with pytest.raises(ValueError):
        security.initialize(key)


def test_raise_value_error_if_value_is_empty_string():
    """The function raises a ValueError if the value is an empty string."""
    key = "secret_key"
    value = ""
    security.initialize(key)
    with pytest.raises(ValueError):
        encrypted_value = security.encrypt(value)
