#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from apps.blueprints.mqttBlueprint import mqtt_blueprint

app = Flask(__name__)
# 读取配置并加载
app.config.from_object(Config)
app.register_blueprint(mqtt_blueprint, url_prefix='/api/device')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
