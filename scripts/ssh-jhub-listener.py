#!/usr/bin/env python3
# Copyright (c) 2021 dciangot
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from ssh_jhub_forwarder import JHubSSHListener
import asyncssh
import asyncio
import sys
import time
from functools import partial


async def start_server():
    await asyncssh.create_server(partial(JHubSSHListener, hub_url="https://jhub.131.154.96.124.myip.cloud.infn.it"), '', 8122,
                                 server_host_keys=['~/.ssh/id_rsa'])

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()
