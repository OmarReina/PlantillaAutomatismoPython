import pytest

from controllers.controller_property import ControllerProperty
from database.database import Database

db_setup: dict = {
    "host": "10.67.51.144",
    "port": "1521",
    "sdi": "QADEV",
    "user": "MDpg2QvA*0SfXPAV81BNH3tqScgkwCw==*SdhJu4gBRKwEYOwa6VWyMw==*FT9zd9jqH9d/ujBwd66FnQ==",
    "password": "fvqbRnJ23XJfLgk=*VgHmaeJiOfdaC8eNjpTFHA==*P5L44+mi9/WDk0HtUkTJnQ==*bUnXD10in7s5SewMb0lUug==",
    "driver": "oracle+cx_oracle",
    "client": "D:\\Drivers\\oracle\\instantclient_11_2"
}

db: Database = Database()
db.initialize("Gl0b@lH1tss", db_setup)
controller_prop = ControllerProperty()


def test_instantiation_success():
    """ControllerProperty object can be instantiated successfully."""
    controller_prop.initialize(db)
    assert isinstance(controller_prop, ControllerProperty)


def test_instantiation_unsuccessful():
    """ControllerProperty object can be instantiated successfully."""
    with pytest.raises(Exception):
        controller_prop.initialize(None)


def test_get_properties_with_invalid_requirement_name():
    controller_prop.initialize(db)
    result = controller_prop.get_properties('requirement1')
    assert isinstance(result, dict)
    assert len(result) == 0


def test_get_properties_with_valid_requirement_name():
    controller_prop.initialize(db)
    result = controller_prop.get_properties('REQ2022_456')
    assert isinstance(result, dict)
    assert len(result) > 0
