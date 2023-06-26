#!/usr/bin/python
# -*- coding: utf-8 -*-
from apps.utils.mqttClient import MQTTClient


class MQTTClientManager:
    def __init__(self, message_storage):
        self.message_storage = message_storage
        self.clients = {}

    def create_client(self, client_id, mac):
        client = MQTTClient(client_id, mac, self.message_storage)
        # client.connect(host, port)
        self.clients[client_id] = client
        return client

    def get_client(self, client_id):
        return self.clients.get(client_id)

    def remove_client(self, client_id):
        client = self.clients.pop(client_id, None)
        if client:
            client.disconnect()

    def connect(self, client_id, host, port):
        return self.clients.get(client_id).connect(host, port)

    def disconnect(self, client_id):
        self.clients.get(client_id).disconnect()
        self.clients.pop(client_id)

    def reconnect(self, client_id):
        self.clients.get(client_id).reconnect()

    def publish(self, client_id, topic, payload):
        self.clients[client_id].publish(topic, payload)

    def get_message_by_trace_id(self, client_id, topic, trace_id):
        return self.message_storage.get_message_by_trace_id(client_id, topic, trace_id)

    def add_preset_message(self, client_id, value):
        self.message_storage.add_preset_message(client_id, value)

    def get_preset_message(self, client_id):
        return self.message_storage.get_preset_message(client_id)

    def client_exist(self, client_id):
        if self.clients.get(client_id, None):
            return True
        return False
