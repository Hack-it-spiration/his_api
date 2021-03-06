import uuid
from copy import deepcopy
from datetime import datetime

from flask import current_app
from mongoengine import Document
from mongoengine.errors import NotUniqueError
from mongoengine.fields import DateTimeField, ReferenceField, StringField, UUIDField
from src.features.common.exceptions import AlreadyExists, UnprocessableEntity
from src.features.common.helpers.pagination import page_to_slice
from src.features.common.helpers.update import update_fields
from src.features.toll_roads.checkpoint.model import Checkpoint


class Segment(Document):

    uuid = UUIDField(binary=False, required=True, unique=True)
    start = ReferenceField(Checkpoint, Required=True)
    end = ReferenceField(Checkpoint, Required=True)
    label = StringField(Required=True)
    created_at = DateTimeField(default=datetime.now, required=True)
    updated_at = DateTimeField(default=datetime.now, required=True)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "start": self.start.uuid,
            "end": self.end.uuid,
            "label": self.label,
            "created_at": self.created_at.strftime(
                current_app.config["DATE_TIME_FORMAT"]
            ),
            "updated_at": self.updated_at.strftime(
                current_app.config["DATE_TIME_FORMAT"]
            ),
        }

    @staticmethod
    def fetch(page, page_size):
        start, end = page_to_slice(page, page_size)
        return list(
            map(
                lambda e: e.to_dict(),
                Segment.objects().order_by("created_at")[start:end],
            )
        )

    @staticmethod
    def insert(segment):
        if "uuid" not in segment:
            segment["uuid"] = str(uuid.uuid4())
        try:
            segment["start"] = Checkpoint.objects(uuid=segment["start"]).get()
            segment["end"] = Checkpoint.objects(uuid=segment["end"]).get()
            return Segment(**segment).save(force_insert=True, validate=True).to_dict()
        except NotUniqueError:
            raise AlreadyExists()
        except KeyError:
            raise UnprocessableEntity()

    @staticmethod
    def alter(uuid, request_body):
        request_body = deepcopy(request_body)
        stored_vehicle = Segment.objects(uuid=uuid).get()
        if "start" in request_body:
            stored_vehicle.start = Checkpoint.objects(uuid=request_body["start"]).get()
            request_body.pop("start")
        if "end" in request_body:
            stored_vehicle.end = Checkpoint.objects(uuid=request_body["end"]).get()
            request_body.pop("end")
        update_fields(request_body, stored_vehicle)
        return stored_vehicle.save(validate=True).to_dict()

    @staticmethod
    def remove(uuid):
        Segment.objects(uuid=uuid).get().delete()
        return uuid
