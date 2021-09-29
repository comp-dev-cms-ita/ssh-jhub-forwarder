import os

import redis

_tls_store_certfile_key = "traefik/tls/stores/default/defaultCertificate/certFile"
_tls_store_certfile_value = "{cert_file}"
_tls_store_keyfile_key = "traefik/tls/stores/default/defaultCertificate/keyFile"
_tls_store_keyfile_value = "{key_file}"
_service_key = "traefik/tcp/services/{name}/loadBalancer/servers/0/address"
_service_value = "{host}:{port}"
_router_rule_key = "traefik/tcp/routers/{name}/rule"
_router_rule_value = "{rule}"
_router_service_key = "traefik/tcp/routers/{name}/service"
_router_service_value = "{service_name}"
_router_tls_key = "traefik/tcp/routers/{name}/tls"
_router_tls_value = "true"


def set_default_certificate(
    key_file: str = "/etc/certs/tls.key", cert_file: str = "/etc/certs/tls.crt"
):

    r = redis_conn()

    check_key_file = r.get(_tls_store_keyfile_key)
    check_cert_file = r.get(_tls_store_certfile_key)

    if check_key_file is None or check_cert_file is None:
        ok = r.set(
            _tls_store_keyfile_key,
            _tls_store_keyfile_value.format(key_file=key_file),
        )
        if not ok:
            raise Exception("cannot set tls default key file")

        ok = r.set(
            _tls_store_certfile_key,
            _tls_store_certfile_value.format(cert_file=cert_file),
        )
        if not ok:
            raise Exception("cannot set tls default cert file")

    r.close()


def redis_conn(
    hostname: str = "localhost", port: int = 6379, password: str = ""
) -> "redis.Redis":
    """Establish a redis connection

    This function checks the following environment variable to establish
    the connection:

        - REDIS_HOSTNAME
        - REDIS_PORT
        - REDIS_PASSWORD

    :return: the redis connection
    :rtype: redis.Redis
    """
    env_hostname = os.getenv("REDIS_HOSTNAME")
    if env_hostname:
        hostname = env_hostname

    env_port = os.getenv("REDIS_PORT")
    if env_port:
        port = int(env_port)

    env_password = os.getenv("REDIS_PASSWORD")
    if env_password:
        password = env_password

    r = redis.Redis(host=hostname, port=port, password=password)
    return r


def set_services(
    name: str = "myservice", host: str = "127.0.0.1", port: int = -1
) -> bool:
    """Set traefic store kv of a service.

    Ref: https://doc.traefik.io/traefik/routing/providers/kv/#services

    :param name: name of the service to insert, defaults to "myservice"
    :type name: str, optional
    :param host: host that will listen, defaults to "127.0.0.1"
    :type host: str, optional
    :param port: port of the service that listen, defaults to -1
    :type port: int, optional
    :raises Exception: Not a valid port integer
    :return: True if the operation went well
    :rtype: bool
    """
    if port <= 0:
        raise Exception("not a valid port integer")

    r = redis_conn()

    res = r.set(
        _service_key.format(name=name), _service_value.format(host=host, port=port)
    )

    r.close()

    return res is True


def set_routers(
    name: str = "myrouter",
    service_name: str = "myservice",
    rule: str = "Host(`example.com`)",
) -> bool:
    """Set traefic store kv of a router

    :param name: name of the router to insert, defaults to "myrouter"
    :type name: str, optional
    :param service_name: name of the associated service, defaults to "myservice"
    :type service_name: str, optional
    :param rule: rule to store, defaults to "Host(`example.com`)"
    :type rule: str, optional
    :raises Exception: empty rule
    :return: True if the operation went well
    :rtype: bool
    """
    if not (len(rule) > 0):
        raise Exception("rule is an empty string")

    r = redis_conn()

    res_rule = r.set(
        _router_rule_key.format(name=name), _router_rule_value.format(rule=rule)
    )
    res_service = r.set(
        _router_service_key.format(name=name),
        _router_service_value.format(service_name=service_name),
    )
    res_tls = r.set(_router_tls_key.format(name=name), _router_tls_value)

    r.close()

    return all([res_rule, res_service, res_tls])


def delete_route_info(router_name: str, service_name: str) -> bool:
    """Delete kv of a stored route

    :param router_name: name of the router
    :type router_name: str
    :param service_name: name of the service associated
    :type service_name: str
    :return: True if the operation went well
    :rtype: bool
    """

    r = redis_conn()

    res = r.delete(_service_key.format(name=service_name))
    res_rule = r.delete(_router_rule_key.format(name=router_name))
    res_service = r.delete(_router_service_key.format(name=router_name))
    res_tls = r.delete(_router_tls_key.format(name=router_name))

    r.close()

    return all([res, res_rule, res_service, res_tls])


if __name__ == "__main__":
    # smoke test redis module
    print(set_services(name="service-1", port=8777))
    print(
        set_routers(
            name="Router-1",
            service_name="service-1",
            rule="HostSNI(`username.192.168.0.1.myip.cloud.blabla.it`)",
        )
    )
    print(delete_route_info(router_name="Router-1", service_name="service-1"))
    set_default_certificate()
