from tortoise import fields
from tortoise.models import Model


class User(Model):
    id: int
    email = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=20)
    username = fields.CharField(max_length=20, unique=True)
    createdAt = fields.DatetimeField(auto_now_add=True)
    modifiedAt = fields.DatetimeField(auto_now=True)

    class Meta:  # type: ignore[]
        table = "users"


class Books(Model):
    title = fields.CharField(max_length=50)
    owner = fields.ForeignKeyField("models.User")
    createdAt = fields.DatetimeField(auto_now_add=True)
    modifiedAt = fields.DatetimeField(auto_now=True)
