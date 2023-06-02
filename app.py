#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from app.config import Config
from app.blueprints.mqttBlueprint import mqtt_blueprint

app = Flask(__name__)
# 读取配置并加载
app.config.from_object(Config)
app.register_blueprint(mqtt_blueprint, url_prefix='/api/device')

if __name__ == '__main__':
    # print(app.url_map)
    app.run(debug=True, port=8000)
