from pydantic import BaseModel


def build_json_object_response_format() -> dict:
    return {
        "type": "json_object",
    }


def build_json_schema_response_format(
    schema: type[BaseModel],
    name: str,
    strict: bool = True,
) -> dict:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": name,
            "strict": strict,
            "schema": schema.model_json_schema(),
        },
    }