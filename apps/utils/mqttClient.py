#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from apps.utils.logger import Logger
from apps.config.config import topic_req, topic_rsp, topic_server
import json
import re
import time

logger = Logger()


class MQTTClient:
    def __init__(self, client_id, mac, message_storage):
        self.client = mqtt.Client(client_id=client_id)
        self.mac = mac
        self.client.username_pw_set(username=mac, password=mac)
        self.client_id = client_id
        self.topic_req = topic_req.format(client_id)
        self.topic_server = topic_server.format(client_id)
        self.topic_rsp = topic_rsp.format(client_id)
        self.client.on_connect = self.on_connect
        # self.client.message_callback_add(self.topic_server, self.handle_preset_message)
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.message_storage = message_storage

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"MQTT connected with client ID: {self.client_id}")
        else:
            logger.info(f"MQTT connection failed with error code {rc}")

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = json.dumps(message.payload.decode())
        logger.info(f"topic:{topic}，来自{client}")
        logger.info(f"payload:{payload}")
        trace_id = re.search(r'traceId.+?:(.*?),', payload).group(1)
        trace_id = trace_id.replace('\\"', "")
        preset_payload = self.message_storage.get_preset_message(self.client_id)
        if topic == topic_server and preset_payload is None:
            self.message_storage.add_message(self.client_id, topic, payload)
            logger.info(f"已保存服务下发到设备{self.client_id}的消息")
            res = {
                "traceId": trace_id,
                "code": 0,
                "msg": "ok",
                "result": {}
            }
            self.client.publish(topic_rsp, json.dumps(res), qos=0)
            time.sleep(0.1)
            logger.info("响应消息成功")
        if preset_payload:
            preset_payload = json.dumps(preset_payload).replace('${TraceId}', trace_id)
            logger.info(f"回复预置响应消息{preset_payload}")
            self.client.publish(topic_rsp, preset_payload, qos=0)
            self.message_storage.del_preset_message(self.client_id)
            time.sleep(0.1)

    def on_disconnect(self, client, userdata, rc):
        if rc == 0:
            logger.info(f"设备{self.client_id}断开连接成功")
        else:
            logger.info(f"设备{self.client_id}意外断开连接,rcCode:{rc},将尝试重连")
            time.sleep(0.3)
            self.client.reconnect()

    def connect(self, host, port):
        return self.client.connect(host, port)

    def start_loop(self):
        # Thread(target=self.client.loop_start()).start()
        self.client.loop_start()

    def disconnect(self):

        self.client.disconnect()

    def reconnect(self):
        self.client.reconnect()

    def publish(self, topic, payload):
        self.client.publish(topic, payload, qos=1)
