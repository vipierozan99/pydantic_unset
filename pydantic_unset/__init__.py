from typing import Any, Self, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class Unset(object):
    __instace = None
    __slots__ = []

    def __new__(cls) -> Self:
        if cls.__instace is None:
            cls.__instace = super().__new__(cls)
        return cls.__instace

    def __repr__(self):
        return "Unset"

    def __str__(self) -> str:
        return "Unset"

    def __bool__(self):
        return False

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: Type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.none_schema(),
            python_schema=core_schema.none_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda c: None
            ),
        )
