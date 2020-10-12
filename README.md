# TCP TLS Tunnel Adapter for Python

Provides functionality for creating a TLS tunnel for HTTP / HTTPS 
requests using the overridden `BaseAdapter` from the `requests` library.

## Usage examples

Let's show, how it works for `requests`.

We should import required modules and declare options:
```python

from tls_tunnel.dto import TunnelOptions, ProxyOptions
from tls_tunnel.constants import Client


tunnel_opts = TunnelOptions(
            host="127.0.0.1",  # tunnel address
            port=1337,  # tunnel port
            auth_login="YOUR_LOGIN",
            auth_password="YOUR_PASSWORD",
            header_secure=True,  # HEADER: secure value True or False
            header_client=Client.CHROME,  # HEADER: imitated Client that will be used
            header_server_name=None  # HEADER: use this option if you will connect to raw IP
        )

# if needed
proxy_opts = ProxyOptions(
        host="your.proxy.host",
        port=1234,
        auth_login="YOUR_LOGIN",
        auth_password="YOUR_PASSWORD",
)
```

Then we can create tunnnel adapter:
```python
from requests import Session
from tls_tunnel.adapter import TunneledHTTPAdapter

adapter = TunneledHTTPAdapter(
            tunnel_opts=tunnel_opts,
            dest_host="howsmyssl.com",  # for example 
            dest_port=443,  # HTTP - 80 | HTTPS - 443
            proxy_options=proxy_opts  # or None if not required
        )

session = Session()

# connect adapter for requests.Session instance
session.mount("http://", self.adapter)
session.mount("https://", self.adapter)
```