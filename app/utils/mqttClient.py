#!/usr/bin/python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from app.utils.logger import Logger
from app.config.config import topic_req, topic_rsp, topic_server
import json
import re

logger = Logger()


class MQTTClient:
    def __init__(self, client_id, message_storage):
        self.client = mqtt.Client(client_id=client_id)
        self.client_id = client_id
        self.topic_req = topic_req.format(client_id)
        self.topic_server = topic_server.format(client_id)
        self.topic_rsp = topic_rsp.format(client_id)
        self.client.on_connect = self.on_connect
        # self.client.message_callback_add(self.topic_server, self.handle_preset_message)
        self.client.on_message = self.on_message
        self.message_storage = message_storage

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"MQTT connected with client ID: {self.client_id}")
            # client.subscribe(self.topic_rsp)
            client.subscribe(self.topic_req)
            client.subscribe(self.topic_server)
        else:
            logger.info(f"MQTT connection failed with error code {rc}")

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = json.dumps(message.payload.decode())
        logger.info(f"订阅的topic:{topic}，来自{client}")
        logger.info(f"payload:{payload}")
        if topic == topic_server.format(self.client_id):
            self.message_storage.add_message(self.client_id, topic, payload)
            logger.info(f"已保存服务下发到设备{self.client_id}的消息")
            request_time = re.search(r'requestTime.+?:(\d+?),', payload).group(1)
            preset_payload = self.message_storage.get_preset_message(self.client_id)
            if preset_payload:
                logger.info(f"回复预置响应消息")
                preset_payload = json.dumps(preset_payload).replace('\"${requestTime}\"', request_time)
                self.publish(self.topic_rsp, preset_payload)
                self.message_storage.del_preset_message(self.client_id)
            else:
                res = {"code": 0, "requestTime": request_time, "result": {}}
                logger.info(f"不是预置响应消息，正常回复")
                self.client.publish(topic_rsp.format(self.client_id), json.dumps(res))

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
        self.client.publish(topic, payload)
