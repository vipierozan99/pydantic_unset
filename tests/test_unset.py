from pydantic import BaseModel

from pydantic_unset import Unset


class MyModel(BaseModel):
    a: int | Unset = Unset()
    b: str | None | Unset = Unset()


def test_from_json():
    json = r"{}"

    model = MyModel.model_validate_json(json)

    print(model)
