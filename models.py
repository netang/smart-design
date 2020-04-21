from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance, Document, fields, validate

db_client = AsyncIOMotorClient('localhost', 27017)
db = db_client['smart_design']
instance = Instance(db)

@instance.register
class Item(Document):
    name = fields.StringField(required=True)
    description = fields.StringField()
    parameters = fields.DictField()

    class Meta:
        collection_name = "items"