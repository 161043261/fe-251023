from pydantic import BaseModel


class GenerateProblemDTO(BaseModel):
    level: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "level": "easy",
            }
        }
    }
