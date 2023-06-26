#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from apps.utils.mqttClientManager import MQTTClientManager
from apps.utils.messageStorage import MessageStorage
from apps.utils.logger import Logger
from apps.config.config import topic_req, topic_server
import json
import traceback

mqtt_blueprint = Blueprint('device', __name__)
message_storage = MessageStorage()
mqtt_manager = MQTTClientManager(message_storage)
logger = Logger()


@mqtt_blueprint.route('/connect', methods=['POST'])
def connect():
    request_data = request.get_json()
    logger.info(f"请求的数据：{request_data}")
    client_id = request_data.get("client_id", None)
    mac = request_data.get("mac", None)
    host = request_data.get("host", None)
    port = request_data.get("port", None)
    if client_id is None:
        return jsonify({"code": 1, "msg": "client_id不能为空"})
    if host is None:
        return jsonify({"code": 1, "msg": "host不能为空"})
    if port is None:
        port = "1883"
    if mac is None:
        return jsonify({"code": 1, "msg": "mac不能为空"})
    try:
        if mqtt_manager.client_exist(client_id):
            mqtt_manager.reconnect(client_id)
            return jsonify({"code": 0, "msg": "connected success", "client_id": client_id})
        else:
            client = mqtt_manager.create_client(client_id, mac)
            rc = client.connect(host, port)
            client.start_loop()
            if rc == 0:
                # logger.info(f"MQTT connected with client ID: {client_id}")
                return jsonify({"code": 0, "msg": "connected success", "client_id": client_id})
            else:
                mqtt_manager.remove_client(client_id)
                return jsonify({"code": rc, "msg": "connected fail", "rc": rc})
    except Exception as e:
        mqtt_manager.remove_client(client_id)
        logger.error(f"Exception:{traceback.format_exc()}")
        return jsonify({"code": 1, "msg": "connected Exception", "msg_exception": str(e)})


@mqtt_blueprint.route('/offline', methods=['POST'])
def offline():
    client_id = request.args.get("client_id")
    if client_id is None:
        return jsonify({"code": 1, "msg": "client_id不能为空"})
    try:
        if mqtt_manager.client_exist(client_id):
            mqtt_manager.disconnect(client_id)
            return jsonify({"code": 0, "msg": "success"})
        else:
            return jsonify({"code": 1, "msg": "device not exist"})
    except Exception as e:
        logger.error(f"Exception:{traceback.format_exc()}")
        return jsonify({"code": 1, "msg": "fail", "errorMsg": str(e)})


@mqtt_blueprint.route('/reconnect', methods=['POST'])
def reconnect():
    client_id = request.args.get("client_id")
    if client_id is None:
        return jsonify({"code": 1, "msg": "client_id不能为空"})
    try:
        if mqtt_manager.client_exist(client_id):
            mqtt_manager.reconnect(client_id)
            return jsonify({"code": 0, "msg": "success"})
        else:
            return jsonify({"code": 1, "msg": "device not exist"})
    except Exception as e:
        logger.error(f"Exception:{traceback.format_exc()}")
        return jsonify({"code": 1, "msg": "fail", "errorMsg": str(e)})


@mqtt_blueprint.route('/upload', methods=['POST'])
def upload():
    client_id = request.args.get("client_id")
    upload_data = request.get_json()
    if client_id is None:
        return jsonify({"code": 1, "msg": "client_id不能为空"})
    topic = topic_req
    try:
        if mqtt_manager.client_exist(client_id):
            mqtt_manager.publish(client_id, topic, json.dumps(upload_data))
            return jsonify({"code": 0, "msg": "success"})
        else:
            return jsonify({"code": 1, "msg": "device not exist"})
    except Exception as e:
        logger.error(f"Exception:{traceback.format_exc()}")
        return jsonify({"code": 1, "msg": "fail", "errorMsg": str(e)})


@mqtt_blueprint.route('/getMsgByTraceId', methods=['POST'])
def get_message_by_trace_id():
    client_id = request.args.get("client_id")
    trace_id = request.get_json().get("traceId")
    topic = topic_server
    logger.info(f"client_id:{client_id},traceId:{trace_id}")
    if client_id is None:
        return jsonify({"code": 1, "msg": "client_id不能为空"})
    if trace_id is None:
        return jsonify({"code": 1, "msg": "trace_id不能为空"})
    try:
        if mqtt_manager.client_exist(client_id):
            msg = mqtt_manager.get_message_by_trace_id(client_id, topic, trace_id)
            if msg == 0:
                return jsonify({"code": 1, "msg": "no msg device"})
            return jsonify({"code": 0, "msg": msg})
        else:
            return jsonify({"code": 1, "msg": "device not exist"})
    except Exception as e:
        logger.error(f"Exception:{traceback.format_exc()}")
        return jsonify({"code": 1, "msg": "no msg device", "errorMsg": str(e)})


@mqtt_blueprint.route('/setResponseMsg', methods=['POST'])
def set_response_message():
    client_id = request.args.get("client_id")
    payload = request.get_json()
    logger.info(f"设备{client_id}需要预置响应消息:\n{payload}")
    if client_id is None:
        return jsonify({"code": 1, "msg": "client_id不能为空"})
    try:
        if mqtt_manager.client_exist(client_id):
            mqtt_manager.add_preset_message(client_id, payload)
            return jsonify({"code": 0, "msg": "success"})
        else:
            return jsonify({"code": 1, "msg": "device not exist"})
    except Exception as e:
        logger.error(f"Exception:{traceback.format_exc()}")
        return jsonify({"code": 1, "msg": "fail", "errorMsg": str(e)})
