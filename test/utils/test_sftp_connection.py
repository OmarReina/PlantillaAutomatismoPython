import pytest
from utils.sftp_connection import SFTPConnection

setup = {
    'host': '100.123.250.29',
    'port': '22',
    'user': 'mediciones',
    'password': 'expe_med27'
}

sftp_connection = SFTPConnection()


def test_instantiation_with_valid_setup():
    """SFTPConnection can be instantiated with a dictionary containing host, port, user, and password keys."""
    sftp_connection.initialize(setup)
    assert isinstance(sftp_connection, SFTPConnection)


def test_connection_error():
    """Connection error"""
    setup = {
        'host': 'example.com',
        'port': '22',
        'user': 'username',
        'password': 'wrong_password'
    }
    sftp_connection.initialize(setup)
    assert sftp_connection.open_connection() == False


def test_connection_with_missing_keys():
    """Connection error"""
    setup = {
        'port': '22',
        'user': 'username',
        'password': 'wrong_password'
    }
    with pytest.raises(Exception):
        sftp_connection.initialize(setup)


def test_connection_establishment():
    """SFTPConnection can establish a connection to an SFTP server."""
    sftp_connection.initialize(setup)
    assert sftp_connection.open_connection() == True


def test_change_directory_warning():
    """SFTPConnection raises a warning if it is unable to change the working directory on the SFTP server."""
    sftp_connection.initialize(setup)

    with pytest.raises(Exception):
        sftp_connection.open_connection()
        sftp_connection.change_path('/invalid_directory')
