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
import os

JHUB_URL = os.environ.get("JHUB_URL")


async def start_server():
    await asyncssh.create_server(
        partial(JHubSSHListener, hub_url=JHUB_URL),
        "",
        8122,
        server_host_keys=["~/.ssh/id_rsa"],
    )


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit("Error starting server: " + str(exc))

loop.run_forever()
