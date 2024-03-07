import pytest
from pydantic import BaseModel, ValidationError
from rich import print

from pydantic_unset import Unset


class MyModel(BaseModel):
    a: int | Unset = Unset()
    b: str | None | Unset = Unset()
    c: str | None | Unset = None


def test_from_python_all_unset():
    value = {}

    m_inst = MyModel.model_validate(value)
    print(m_inst)

    assert m_inst.a is Unset()
    assert m_inst.a is not None
    assert m_inst.b is Unset()
    assert m_inst.b is not None
    assert m_inst.c is None
    assert m_inst.c is not Unset()

    model_dump = m_inst.model_dump()
    print(model_dump)
    assert model_dump == {"a": None, "b": None, "c": None}

    model_dump = m_inst.model_dump(exclude_none=True)
    print(model_dump)
    assert model_dump == {"a": None, "b": None}

    model_dump = m_inst.model_dump(exclude_unset=True)
    print(model_dump)
    assert (
        model_dump == {}
    )  # TODO: this can feel a bit unintuitive, bc the default is None, but since we didn't set it, it's not in __fields_set__

    model_dump = m_inst.model_dump(exclude_none=True, exclude_unset=True)
    print(model_dump)
    assert model_dump == {}


def test_from_json_all_unset():
    json = r"{}"

    m_inst = MyModel.model_validate_json(json)
    print(m_inst)

    assert m_inst.a is Unset()
    assert m_inst.a is not None
    assert m_inst.b is Unset()
    assert m_inst.b is not None
    assert m_inst.c is None
    assert m_inst.c is not Unset()

    model_dump = m_inst.model_dump()
    print(model_dump)
    assert model_dump == {"a": None, "b": None, "c": None}

    model_dump = m_inst.model_dump(exclude_none=True)
    print(model_dump)
    assert model_dump == {"a": None, "b": None}

    model_dump = m_inst.model_dump(exclude_unset=True)
    print(model_dump)
    assert (
        model_dump == {}
    )  # TODO: this can feel a bit unintuitive, bc the default is None, but since we didn't set it, it's not in __fields_set__

    model_dump = m_inst.model_dump(exclude_none=True, exclude_unset=True)
    print(model_dump)
    assert model_dump == {}


def test_from_python_set_to_none():
    value = {"a": None, "b": None, "c": None}

    with pytest.raises(ValidationError) as e:
        m_inst = MyModel.model_validate(value)  # TODO: this should raise
        print(m_inst)

    json = r'{"a": 1, "b": null, "c": null}'

    m_inst = MyModel.model_validate_json(json)
    print(m_inst)

    assert m_inst.a == 1
    assert m_inst.b is None
    assert m_inst.c is None

    model_dump = m_inst.model_dump()
    print(model_dump)
    assert model_dump == {"a": 1, "b": None, "c": None}

    model_dump = m_inst.model_dump(exclude_none=True)
    print(model_dump)
    assert model_dump == {"a": 1}

    model_dump = m_inst.model_dump(exclude_unset=True)
    print(model_dump)
    assert model_dump == {"a": 1, "b": None, "c": None}

    model_dump = m_inst.model_dump(exclude_none=True, exclude_unset=True)
    print(model_dump)
    assert model_dump == {"a": 1}


def test_from_json_set_to_none():
    json = r'{"a": null, "b": null, "c": null}'

    with pytest.raises(ValidationError) as e:
        m_inst = MyModel.model_validate_json(json)  # TODO: this should raise
        print(m_inst)

    json = r'{"a": 1, "b": null, "c": null}'

    m_inst = MyModel.model_validate_json(json)
    print(m_inst)

    assert m_inst.a == 1
    assert m_inst.b is None
    assert m_inst.c is None

    model_dump = m_inst.model_dump()
    print(model_dump)
    assert model_dump == {"a": 1, "b": None, "c": None}

    model_dump = m_inst.model_dump(exclude_none=True)
    print(model_dump)
    assert model_dump == {"a": 1}

    model_dump = m_inst.model_dump(exclude_unset=True)
    print(model_dump)
    assert model_dump == {"a": 1, "b": None, "c": None}

    model_dump = m_inst.model_dump(exclude_none=True, exclude_unset=True)
    print(model_dump)
    assert model_dump == {"a": 1}


def test_json_schema():
    model_json_schema = MyModel.model_json_schema()

    assert model_json_schema == {
        "title": "MyModel",
        "type": "object",
        "properties": {
            "a": {
                "title": "A",
                "type": "integer",
            },
            "b": {
                "title": "B",
                "anyOf": [
                    {"type": "string"},
                    {"type": "null"},
                ],
            },
            "c": {
                "title": "C",
                "anyOf": [
                    {"type": "string"},
                    {"type": "null"},
                ],
                "default": None,
            },
        },
    }
