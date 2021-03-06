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


class TunneledHTTPAdapter(BaseAdapter):

    def __init__(self,
                 tunnel_opts: TunnelOptions,
                 dest_host: str,
                 dest_port: int,
                 proxy_options: ProxyOptions = None):
        super(BaseAdapter, self).__init__()
        self.tunnel_opts = tunnel_opts
        self.dest_host = dest_host
        self.dest_port = dest_port
        self.proxy_url = generate_proxy_url(proxy=proxy_options)

    def close(self):
        pass

    def send(self, request, **kwargs):
        connection = create_tunnel_connection(
            tunnel_opts=self.tunnel_opts,
            dest_host=self.dest_host,
            dest_port=self.dest_port,
            proxy_url=self.proxy_url
        )
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

        connection.close()
        return response
