from tortoise.models import Model
from tortoise import fields

class Narrations(Model):
    id = fields.IntField(pk=True)
    narration = fields.TextField()

class Facts(Model):
    id = fields.IntField(pk=True)
    fact = fields.TextField()
    narration = fields.ForeignKeyField('models.Narrations', related_name='facts')

class Scenes(Model):
    id = fields.IntField(pk=True)
    scene = fields.TextField()
    narration = fields.ForeignKeyField('models.Narrations', related_name='scenes')

class Sounds(Model):
    id = fields.IntField(pk=True)
    sound = fields.TextField()
    narration = fields.ForeignKeyField('models.Narrations', related_name='sounds')

class Errors(Model):
    id = fields.IntField(pk=True)
    error = fields.TextField()
    narration = fields.ForeignKeyField('models.Narrations', related_name='errors')