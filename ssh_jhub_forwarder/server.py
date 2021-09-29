# Copyright (c) 2021 dciangot
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys

import asyncssh
from aiohttp import ClientSession

from .dbcache import (
    delete_route_info,
    set_routers,
    set_services,
    set_default_certificate,
)


class DaskSSHServer(asyncssh.SSHServer):
    def __init__(self, hub_url=None, *args, **kwargs):
        self.hub_url = hub_url
        self.router_name = None

        super().__init__(*args, **kwargs)

        set_default_certificate()

    def server_requested(self, listen_host: str, listen_port: int) -> bool:
        """Create a route for the user service.

        If there are redis exception check out the database connection and
        the dbcache module.

        :param listen_host: an ip that have to liste
        :type listen_host: str
        :param listen_port: a port to listen
        :type listen_port: int
        :return: if the operation went well
        :rtype: bool
        """
        route = set_routers(
            name=self.username,
            service_name=self.username,
            rule="HostSNI(`{}`)".format(self.username),
        )
        service = set_services(name=self.username, port=listen_port)

        self.router_name = self.username
        return all([route, service])

    def connection_made(self, conn):
        print("SSH connection received from %s." % conn.get_extra_info("peername")[0])

    def connection_lost(self, exc):
        """Remove the ssh connection and the route info.

        :param exc: the ssh executable
        :type exc: process
        :raises Exception: Failed to delete route for
        """
        if not delete_route_info(
            router_name=self.router_name, service_name=self.router_name
        ):
            raise Exception(f"Failed to delete route for {self.router_name}")
        if exc:
            print("SSH connection error: " + str(exc), file=sys.stderr)
        else:
            print("SSH connection closed.")

    def begin_auth(self, username):
        return True

    def password_auth_supported(self):
        return True

    async def validate_password(self, username, password):
        self.username = username
        self.token = password

        headers = {"Authorization": f"token {self.token}"}

        # TODO: use hub/api/authorizations/token API to validate user
        # 403: token not valid
        # 404: user not found
        async with ClientSession(headers=headers) as session:
            check_url = "{}/hub/api/users/{}".format(
                self.hub_url, username.split("-")[0]
            )
            async with session.get(check_url, ssl=False) as resp:
                print(resp.status)
                if resp.status == 200:
                    return True
                else:
                    return False


class DaskSSHListener(DaskSSHServer):
    def __init__(self, hub_url=None, *args, **kwargs):
        super().__init__(hub_url=hub_url, *args, **kwargs)

    def server_requested(self, listen_host: str, listen_port: int) -> bool:
        """Disable remote listener"""
        print("server requested {}, {}".format(listen_host, listen_port))
        return False

    def connection_requested(self, dest_host, dest_port, orig_host, orig_port):
        # TODO: check redis if the port is allowed for that username
        print(
            "connection request {}, {}, {}, {}".format(
                dest_host, dest_port, orig_host, orig_port
            )
        )
        return True

    def connection_lost(self, exc):
        """Remove the ssh connection and the route info.

        :param exc: the ssh executable
        :type exc: process
        :raises Exception: Failed to delete route for
        """
        if exc:
            print("SSH connection error: " + str(exc), file=sys.stderr)
        else:
            print("SSH connection closed.")
