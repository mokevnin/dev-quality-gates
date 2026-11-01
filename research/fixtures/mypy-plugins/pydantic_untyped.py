from pydantic import BaseModel


class User(BaseModel):
    name: str
    age = 1


def years(user: User) -> int:
    return user.age
