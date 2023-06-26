#!/usr/bin/python
# -*- coding: utf-8 -*-
host = '127.0.0.1'
port = 1883
# topic_req = "mqtt/{}/v1/req"  # IOT设备主动上报
# topic_rsp = "mqtt/{}/v1/bypass/rsp"  # IOT设备主动响应服务器
# topic_server = "mqtt/{}/v1/bypass"  # 服务向IOT设备下发指令
topic_req = "report"
topic_server = "request"
topic_rsp = "response"
