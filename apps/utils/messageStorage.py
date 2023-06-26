#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from apps.utils.logger import Logger
import re
from threading import Lock
import json

logger = Logger()


class MessageStorage:
    def __init__(self):
        self.messages = []
        self.preset_message = {}
        self.lock_message = Lock()

    def add_message(self, client_id, topic, payload):
        self.lock_message.acquire()
        if len(self.messages) > 50:
            self.messages.pop()
        self.messages.append({"client_id": client_id, "topic": topic, "payload": payload})
        self.lock_message.release()

    def get_message_by_trace_id(self, client_id, topic, trace_id):
        response_msg = []
        for msg in self.messages:
            payload = msg.get("payload")
            logger.info(f"存设备的信息:{msg}")
            client_id_p = msg.get("client_id", None)
            topic_p = msg.get("topic", None)
            logger.info(f"topic:{topic_p},client_id:{client_id_p}")
            if client_id_p == client_id and topic_p == topic:
                logger.info(f"存在符合相关设备的信息:{payload}")
                trace_id_payload = re.search(r'traceId.+?:(.*?),', payload).group(1)
                trace_id_payload = trace_id_payload.replace('\\"', "")
                logger.info(f"traceId:{trace_id_payload}")
                if trace_id_payload == trace_id:
                    response_msg.append(payload)
        if len(response_msg) == 1:
            return response_msg[0]
        if len(response_msg) == 0:
            return 0
        return "|".join(response_msg)

    def add_preset_message(self, client_id, value):
        self.preset_message[client_id] = value

    def get_preset_message(self, client_id):
        return self.preset_message.get(client_id, None)

    def del_preset_message(self, client_id):
        return self.preset_message.pop(client_id)
