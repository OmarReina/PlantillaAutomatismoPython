from models.model_property import ModelProperty


def test_instantiation_success():
    """ModelProperty object can be instantiated successfully."""
    model_prop = ModelProperty()
    assert isinstance(model_prop, ModelProperty)


def test_initialize_properties_to_none():
    """Creating a new instance of ModelProperty should initialize all its properties to None."""
    model_property = ModelProperty()
    assert model_property.id_propiedad is None
    assert model_property.nombre_propiedad is None
    assert model_property.valor_propiedad is None
    assert model_property.rq is None
    assert model_property.descripcion is None


def test_set_properties_update_values():
    """Setting the properties of a ModelProperty instance should update the corresponding values."""
    model_property = ModelProperty()
    model_property.id_propiedad = 1
    model_property.nombre_propiedad = "Test Property"
    model_property.valor_propiedad = "Test Value"
    model_property.rq = "Test RQ"
    model_property.descripcion = "Test Description"

    assert model_property.id_propiedad == 1
    assert model_property.nombre_propiedad == "Test Property"
    assert model_property.valor_propiedad == "Test Value"
    assert model_property.rq == "Test RQ"
    assert model_property.descripcion == "Test Description"
