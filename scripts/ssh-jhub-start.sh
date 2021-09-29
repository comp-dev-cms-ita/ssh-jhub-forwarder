#!/bin/bash
# Copyright (c) 2021 dciangot
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

ssh-keygen -f /root/.ssh/id_rsa -N ""

ssh-jhub-forwarder.py