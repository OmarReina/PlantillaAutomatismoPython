import pytest

from models.model_requirement import ModelRequirement

configurations_dict = {"environment": "DEV",
                       "log_file": "log.log",
                       "name": "REQ0000_000",
                       "secret_key": "app_secret_key",
                       "version": "app_version"
                       }

configurations_dict2 = {"environment": "app_environment",
                        "log_file": "app_log_file",
                        "name": "app_requirement_name",
                        "secret_key": "app_secret_key",
                        "version": "app_version"
                        }
model_req = ModelRequirement()


def test_instantiation_success():
    """ModelRequirement object can be instantiated successfully."""
    model_req.initialize(configurations=configurations_dict,
                         environment=configurations_dict["environment"],
                         log_file=configurations_dict["log_file"],
                         name=configurations_dict["name"],
                         secret_key=configurations_dict["secret_key"],
                         version=configurations_dict["version"])
    assert isinstance(model_req, ModelRequirement)


def test_set_and_get_properties():
    """The object's properties can be set and retrieved successfully."""
    model_req.initialize(configurations=configurations_dict,
                         environment=configurations_dict["environment"],
                         log_file=configurations_dict["log_file"],
                         name=configurations_dict["name"],
                         secret_key=configurations_dict["secret_key"],
                         version=configurations_dict["version"])
    properties = {'property1': 'value1', 'property2': 'value2'}
    model_req.set_properties(properties)
    assert model_req.get_properties() == properties


def test_get_name_value():
    """The get object's name property  value"""
    model_req.initialize(configurations=configurations_dict,
                         environment=configurations_dict["environment"],
                         log_file=configurations_dict["log_file"],
                         name=configurations_dict["name"],
                         secret_key=configurations_dict["secret_key"],
                         version=configurations_dict["version"])
    name = 'REQ0000_000'
    assert model_req.get_name() == name
