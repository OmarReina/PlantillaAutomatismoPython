from utils.validation import Validation


def test_check_missing_keys_all_attributes_present():
    """check_missing_keys returns True and "Los atributos existen."
    message when all attributes are present in the dictionary"""
    attributes = {'attribute1', 'attribute2', 'attribute3'}
    dictionary = {'attribute1': 'value1', 'attribute2': 'value2', 'attribute3': 'value3'}
    result, message = Validation.check_missing_keys(attributes, dictionary)
    assert result == True


def test_check_missing_keys_some_attributes_missing():
    """check_missing_keys returns False and "Faltan los siguientes atributos: [...]"
    message when some attributes are missing from the dictionary"""
    attributes = {'attribute1', 'attribute2', 'attribute3'}
    dictionary = {'attribute1': 'value1', 'attribute3': 'value3'}
    result, message = Validation.check_missing_keys(attributes, dictionary)
    assert result == False
    assert message == "Faltan los siguientes atributos: ['attribute2']"


def test_check_missing_keys_exception_raised():
    """check_missing_keys returns False and "Error validando atributos: [...]"
    message when an exception is raised during execution"""
    attributes = {'attribute1', 'attribute2', 'attribute3'}
    dictionary = {}
    result, message = Validation.check_missing_keys(attributes, dictionary)
    assert result == False


def test_check_missing_keys_empty_attributes_and_dictionary():
    """check_missing_keys returns True and "Los atributos existen." message when attributes and dictionary are empty"""
    attributes = set()
    dictionary = {}
    result, message = Validation.check_missing_keys(attributes, dictionary)
    assert result == False


def test_check_attribute_non_empty_string():
    """check_string_value returns True and "El valor es valido." message when value is a non-empty string"""
    value = "non_empty_string"
    result, message = Validation.check_attribute(value)
    assert result == True


def test_check_attribute_empty_string():
    """check_string_value returns True and "El valor es valido." message when value is a non-empty string"""
    value = ""
    result, message = Validation.check_attribute(value)
    assert result == False


def test_check_attribute_non_empty_dictionary():
    """check_string_value returns True and "El valor es valido." message when value is a non-empty string"""
    value = {"prueba": "non_empty_string"}
    result, message = Validation.check_attribute(value)
    assert result == True


def test_check_attribute_empty_dictionary():
    """check_string_value returns True and "El valor es valido." message when value is a non-empty string"""
    value = {}
    result, message = Validation.check_attribute(value)
    assert result == False


def test_check_attribute_none_value():
    """check_string_value returns True and "El valor es valido." message when value is a non-empty string"""
    value = None
    result, message = Validation.check_attribute(value)
    assert result == False

