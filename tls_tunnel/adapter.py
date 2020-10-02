import requests

import requests.cookies
import requests.utils
from http.client import HTTPConnection
from requests.structures import CaseInsensitiveDict
from requests.adapters import BaseAdapter

from tls_tunnel.dto import TunnelOptions, ProxyOptions
from tls_tunnel.utils import generate_basic_header, generate_proxy_url


def create_tunnel_connection(tunnel_opts: TunnelOptions,
                             dest_host: str,
                             dest_port: int,
                             proxy_url: str = None):

    conn = HTTPConnection(tunnel_opts.host, tunnel_opts.port)
    headers = {
        "Authorization": generate_basic_header(tunnel_opts.auth_login,
                                               tunnel_opts.auth_password),
        "Client": tunnel_opts.header_client,
        "Connection": 'keep-alive',
        "Server-Name": tunnel_opts.header_server_name or dest_host,
        "Host": tunnel_opts.host,
        "Secure": str(int(tunnel_opts.header_secure)),
    }

    if proxy_url:
        headers["Proxy"] = proxy_url

    conn.set_tunnel(dest_host, port=dest_port, headers=headers)
    conn.connect()
    return conn


def prepare_http_adapter(tunnel_opts: TunnelOptions,
                         dest_host: str,
                         dest_port: int,
                         proxy: ProxyOptions = None):

    proxy_url = generate_proxy_url(proxy=proxy)
    tunneled_connection = create_tunnel_connection(
        tunnel_opts=tunnel_opts,
        dest_host=dest_host,
        dest_port=dest_port,
        proxy_url=proxy_url
    )

    class TunneledHTTPAdapter(BaseAdapter):

        def close(self):
            pass

        def send(self, request, **kwargs):
            connection = tunneled_connection
            connection.request(method=request.method,
                               url=request.url,
                               body=request.body,
                               headers=request.headers)
            r = connection.getresponse()
            response = requests.Response()
            response.status_code = r.status
            response.headers = CaseInsensitiveDict(r.headers)
            response.raw = r
            response.reason = r.reason
            response.url = request.url
            response.request = request
            response.connection = connection
            response.encoding = requests.utils.get_encoding_from_headers(response.headers)
            requests.cookies.extract_cookies_to_jar(response.cookies, request, r)
            return response

    return TunneledHTTPAdapter()
