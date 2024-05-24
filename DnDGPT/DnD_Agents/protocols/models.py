from tortoise.models import Model
from tortoise import fields

class Actions(Model):
    id = fields.IntField(pk=True)
    action = fields.TextField()
    

class Narrations(Model):
    id = fields.IntField(pk=True)
    narration = fields.TextField()
    action = fields.ForeignKeyField('models.Actions', related_name='narrations')

class Facts(Model):
    id = fields.IntField(pk=True)
    fact = fields.TextField()
    action = fields.ForeignKeyField('models.Actions', related_name='facts')

class Scenes(Model):
    id = fields.IntField(pk=True)
    scene = fields.TextField()
    action = fields.ForeignKeyField('models.Actions', related_name='scenes')

class Sounds(Model):
    id = fields.IntField(pk=True)
    sound = fields.TextField()
    action = fields.ForeignKeyField('models.Actions', related_name='sounds')

class Errors(Model):
    id = fields.IntField(pk=True)
    error = fields.TextField()
    action = fields.ForeignKeyField('models.Actions', related_name='errors')


    
