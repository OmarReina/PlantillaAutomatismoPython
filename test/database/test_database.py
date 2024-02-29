import pytest
from sqlalchemy import orm
from database.database import Database

setup = {
        'host': '10.67.51.144',
        'port': '1521',
        'sdi': 'QADEV',
        'user': 'MDpg2QvA*0SfXPAV81BNH3tqScgkwCw==*SdhJu4gBRKwEYOwa6VWyMw==*FT9zd9jqH9d/ujBwd66FnQ==',
        'password': 'fvqbRnJ23XJfLgk=*VgHmaeJiOfdaC8eNjpTFHA==*P5L44+mi9/WDk0HtUkTJnQ==*bUnXD10in7s5SewMb0lUug==',
        'driver': 'oracle+cx_oracle',
        'client': 'D:\\Drivers\\oracle\\instantclient_11_2'
    }

key = 'test_key'

database: Database = Database()


def test_object_created_successfully():
    """Database object is created successfully with valid setup and key"""
    database.initialize(key, setup)
    assert isinstance(database, Database)


def test_get_attributes_returns_set_of_attributes():
    """get_attributes() method returns a set of attributes"""
    database.initialize(key, setup)
    attributes = database.get_attributes()
    assert isinstance(attributes, set)


def test_get_session_returns_valid_session_object():
    """get_session() method returns a valid session object"""
    database.initialize(key, setup)
    session = database.get_session()
    assert isinstance(session, orm.Session)


def test_object_not_created_if_setup_missing():
    """Database object is not created if setup is missing"""
    setup = {}
    with pytest.raises(Exception):
        database.initialize(key, setup)


def test_object_not_created_if_attribute_missing_in_setup():
    """Database object is not created if attribute missing in setup"""
    setup = {
        'host': 'localhost',
        'port': '1521',
        'sdi': 'XE',
        'user': 'test_user',
        'password': 'test_password',
        'driver': 'oracle'
    }

    with pytest.raises(Exception):
        database.initialize(key, setup)


def test_security_object_not_created_if_key_invalid():
    """Security object is not created if key is invalid"""
    key = ''

    with pytest.raises(Exception):
        database.initialize(key, setup)
