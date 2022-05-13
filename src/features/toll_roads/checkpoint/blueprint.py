from flask import Blueprint, jsonify, request

from .controller import create_handler, delete_handler, get_handler, update_handler

checkpoints = Blueprint("checkpoints", __name__, url_prefix="/checkpoints")


@checkpoints.route("", methods=["GET"])
def get():
    return jsonify(get_handler(request.args))


@checkpoints.route("", methods=["POST"])
def create():
    request_body = request.get_json()
    response = create_handler(request_body)
    return jsonify(response)


@checkpoints.route("/<uuid:uuid>", methods=["DELETE"])
def delete(uuid):
    response = delete_handler(uuid)
    return jsonify(response)


@checkpoints.route("/<uuid:uuid>", methods=["PATCH"])
def update(uuid):
    request_body = request.get_json()
    response = update_handler(request_body, uuid)
    return jsonify(response)
