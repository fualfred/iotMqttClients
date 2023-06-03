#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
from logging import handlers


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        # file_name_date = time.strftime("%Y-%m-%d", time.localtime())
        self.file_name = os.path.join(os.path.dirname(__name__), "log/iotDevice.log")
        formatter = logging.Formatter('%(asctime)s -%(filename)s-%(funcName)s-%(lineno)s- %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.file_name, mode="a", encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        th = handlers.RotatingFileHandler(self.file_name, mode='a', maxBytes=1024*1024*3, backupCount=5, encoding="utf-8")
        th.setLevel(level)
        th.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(th)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
