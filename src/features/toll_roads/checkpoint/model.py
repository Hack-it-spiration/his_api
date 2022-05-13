import uuid

from mongoengine import Document
from mongoengine.errors import NotUniqueError, ValidationError
from mongoengine.fields import GeoPointField, StringField, UUIDField
from src.features.common.exceptions import AlreadyExists
from src.features.common.helpers.update_helpers import update_fields


def validate_GeoPoint(value):
    try:
        longitude, latitude = value
        if longitude < -180 or latitude < -90:
            raise ValidationError("Integer value is too small")
        if longitude > 180 or latitude > 90:
            raise ValidationError("Integer value is too large")
    except (ValueError, TypeError):
        pass


class Checkpoint(Document):
    uuid = UUIDField(binary=False, required=True, unique=True)
    label = StringField(required=True)
    location = GeoPointField(required=True, validation=validate_GeoPoint)

    def to_dict(self):
        return {"uuid": self.uuid, "label": self.label, "location": self.location}

    @staticmethod
    def fetch():
        return list(map(lambda e: e.to_dict(), Checkpoint.objects()))

    @staticmethod
    def insert(checkpoint):
        if "uuid" not in checkpoint:
            checkpoint["uuid"] = str(uuid.uuid4())
        try:
            return (
                Checkpoint(**checkpoint)
                .save(force_insert=True, validate=True)
                .to_dict()
            )
        except NotUniqueError:
            raise AlreadyExists()

    @staticmethod
    def alter(uuid, request_body):
        stored_vehicle = Checkpoint.objects(uuid=uuid).get()
        update_fields(request_body, stored_vehicle)
        return stored_vehicle.save(validate=True).to_dict()

    @staticmethod
    def remove(uuid):
        Checkpoint.objects(uuid=uuid).get().delete()
        return uuid
