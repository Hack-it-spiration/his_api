from mongoengine import Document
from mongoengine.fields import UUIDField, StringField, ReferenceField

from features.toll_roads.checkpoint.model import Checkpoint


class Segment(Document):

    uuid = UUIDField(binary=False, required=True, unique=True)
    start = ReferenceField(Checkpoint, Required=True)
    end = ReferenceField(Checkpoint, Required=True)
    name = StringField(Required=True)
