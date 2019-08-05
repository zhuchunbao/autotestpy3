#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import configparser
import os
def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/settings.conf'
    config.read(path)
    return config.get(section, key)