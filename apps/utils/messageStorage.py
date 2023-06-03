#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from apps.utils.logger import Logger
import re
from threading import Lock

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

    def get_message_by_request_time(self, client_id, topic, request_time):
        response_msg = []
        for msg in self.messages:
            payload = msg.get("payload")
            logger.info(f"存设备的信息:{msg}")
            client_id_p = msg.get("client_id", None)
            topic_p = msg.get("topic", None)
            logger.info(f"topic:{topic_p},client_id:{client_id_p}")
            if client_id_p == client_id and topic_p == topic:
                logger.info(f"存在符合相关设备的信息:{payload}")
                request_time_payload = re.search(r'requestTime.+?:(\d+?),', payload).group(1)
                logger.info(f"requestTime:{request_time_payload}")
                if int(request_time_payload) == int(request_time):
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
