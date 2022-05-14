import traceback

from flask import Blueprint, jsonify, request
from src.features.common.response_handlers import success_response

from ..toll_roads.segment.model import Segment
from .api.api_call_pred import api_call

model = Blueprint("model", __name__)


@model.route("/prediction", methods=["POST"])
def prediction():
    req_data = request.get_json()
    _uuid = req_data["uuid"]
    segment = Segment.objects(uuid=_uuid).get()

    origin = ",".join([str(_) for _ in segment.start.location])
    origin_name = segment.start.label
    destination = ",".join([str(_) for _ in segment.end.location])
    destination_name = segment.end.label
    try:
        out = api_call(origin, destination, origin_name, destination_name)
        return success_response(out)
    except Exception as e:
        return jsonify({"message": traceback.format_exc()})
