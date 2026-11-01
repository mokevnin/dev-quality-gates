from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str


def mutate(user: User) -> None:
    user.name = "no"
