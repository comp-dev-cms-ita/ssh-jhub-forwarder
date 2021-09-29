# ssh-jhub-forwarder

A tool for enabling ssh remote and local port forwarding via SSH and authentication with JupyterHUB application tokens.

- ssh-forwader: the agent responsible for remote ssh forwarding
- ssh-listener: the agent responsible for the local ssh forwarding

## Adoption

This solution is adopted to allow external agents to connect and interact with JupyterLab plugins and extesions, e.g. an HTCondor worker node exposing a service for a Dask client running on a separate JupyterHUB instance

```text
+----------------------------------------------------------+              +----------------------------------+
|                                                          |              |                                  |
|   JupyterHUB k8s cluster                                 |              |                                  |
|                                                          |              |   Private network cluster        |
|                                    +---------------------+              |                                  |
|                                    |                     |              |                                  |
|     +--------------+               +--------+   +--------+              |             +--------------+     |
|     |              |               |        |   |        |              |             |              |     |
|     |  JupyterLab  <---------------+ ssh    <---+ ssh    <--------------+-------------+  Remote      |     |
|     |   extension  |               | listen |   | fwd    |              |             |  Application |     |
|     |              |               |        |   |        |              |             |              |     |
|     +--------------+               +--------+   +--------+              |             +--------------+     |
|                                    |                     |              |                                  |
|                                    +---------------------+              |                                  |
|                                                          |              |                                  |
+----------------------------------------------------------+              +----------------------------------+
```
