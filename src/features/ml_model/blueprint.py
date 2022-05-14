import datetime
import json
import traceback

from flask import Blueprint, jsonify, request

from ..toll_roads.segment.model import Segment
from .api.api_call_pred import api_call

model = Blueprint("model", __name__)

# API to get user inputs


@model.route("/prediction", methods=["POST"])
def prediction():
    try:
        req_data = request.get_json()
        _uuid = req_data["uuid"]
        date_time = req_data["datetime"]
        segment = Segment.objects(uuid=_uuid).get()

        origin = ",".join([str(_) for _ in segment.start.location])
        origin_name = segment.start.label
        destination = ",".join([str(_) for _ in segment.end.location])
        destination_name = segment.end.label
        # print(origin)

        # origin = req_data["origin"]
        # destination = req_data["destination"]
        # origin_name = "London"
        # destination_name = ""
        # process time
        tm = datetime.datetime.strptime(date_time, "%Y/%m/%d %H:%M").strftime(
            "%Y-%m-%dT%H:%M"
        )

        out = api_call(origin, destination, origin_name, destination_name, tm)

        return json.dumps(out)
        # return ""

    except:

        return jsonify({"trace": traceback.format_exc()})
