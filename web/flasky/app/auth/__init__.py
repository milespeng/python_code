#!/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"

from flask import Blueprint

auth=Blueprint('auth',__name__)

from . import views
