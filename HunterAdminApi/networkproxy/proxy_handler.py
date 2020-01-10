#!/usr/bin/env python
'''
owtf is an OWASP+PTES-focused try to unite great tools & facilitate pentesting
Copyright (c) 2013, Abraham Aranguren <name.surname@gmail.com>  http://7-a.org
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the copyright owner nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Inbound Proxy Module developed by Bharadwaj Machiraju (blog.tunnelshade.in)
#                     as a part of Google Summer of Code 2013

# Modified by md5_salt (5alt.me)
# Modified by b5mali4
'''
import base64
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.curl_httpclient
import socket
import ssl
import tornado.escape
import tornado.httputil
import os
from networkproxy.socket_wrapper import wrap_socket
from networkproxy import CACERT_FILE
from networkproxy import CAKEY_FILE
from networkproxy import CERT_DIR
from networkproxy import get_http_server


class HttpRequestUtil():
    @staticmethod
    def generate_request_url(request: tornado.httputil.HTTPServerRequest) -> str:
        """
        根据实际请求生成url
        :param self: 
        :return: 
        """
        assert isinstance(request, tornado.httputil.HTTPServerRequest)
        if request and request.host in request.uri.split('/'):  # Normal Proxy Request
            url = request.uri
        else:  # Transparent Proxy Request
            url = request.protocol + "://" + request.host + request.uri

        return url

    @staticmethod
    def format_request_headers(request: tornado.httputil.HTTPServerRequest) -> dict:
        """
        格式化请求头
        :return: 
        """
        assert isinstance(request, tornado.httputil.HTTPServerRequest)
        headers = dict()
        if not request.headers:
            return headers
        for (header_name, header_value) in request.headers.items():
            if header_name not in ('Connection', 'Cache-Control', 'Content-Length'):
                headers[header_name] = header_value
        return headers


class ProxyHandler(tornado.web.RequestHandler):
    """
    This RequestHandler processes all the requests that the application recieves
    """
    SUPPORTED_METHODS = ['GET', 'POST', 'CONNECT', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    # Data for handling headers through a streaming callback
    RESTRICTED_HEADERS = ('Content-Length', 'Content-Encoding', 'Etag', 'Transfer-Encoding', 'Connection', 'Vary',
                          'Accept-Ranges', 'Pragma')

    response_body = None

    def finish(self):
        """
        结束页面
        :return: 
        """
        if not self._finished:
            tornado.web.RequestHandler.finish(self)

    def handle_response(self, response):
        """
        This function is a callback after the async client gets the full response
        This method will be improvised with more headers from original responses
        :param response: 
        :return: 
        """

        self.response_body = response.body if response.body else self.response_body

        if self.response_body and not self._finished:
            self.write(self.response_body)

        self.set_status(response.code)
        for header, value in list(response.headers.items()):
            if header == "Set-Cookie":
                self.add_header(header, value)
            else:
                if header not in ProxyHandler.RESTRICTED_HEADERS:
                    self.set_header(header, value)
        self.finish()

    # This function is a callback when a small chunk is recieved
    def handle_data_chunk(self, data):
        if data:
            if not self.response_body:
                self.response_body = data
            else:
                self.response_body += data

    @tornado.web.asynchronous
    def get(self):
        """
        * This function handles all requests except the connect request.
        * Once ssl stream is formed between browser and proxy, the requests are
          then processed by this function
        """
        request_url = HttpRequestUtil.generate_request_url(request=self.request)
        request_headers = HttpRequestUtil.format_request_headers(self.request)
        async_client = tornado.curl_httpclient.CurlAsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest(
            url=request_url,
            method=self.request.method,
            body=self.request.body if self.request.method != 'GET' else None,
            headers=request_headers,
            follow_redirects=False,
            use_gzip=True,
            streaming_callback=self.handle_data_chunk,
            header_callback=None,
            proxy_host=self.application.outbound_ip,
            proxy_port=self.application.outbound_port,
            allow_nonstandard_methods=True,
            validate_cert=False)

        try:
            async_client.fetch(request, callback=self.handle_response)
        except Exception as e:
            print(e)

    # The following 5 methods can be handled through the above implementation
    @tornado.web.asynchronous
    def post(self):
        return self.get()

    @tornado.web.asynchronous
    def head(self):
        return self.get()

    @tornado.web.asynchronous
    def put(self):
        return self.get()

    @tornado.web.asynchronous
    def delete(self):
        return self.get()

    @tornado.web.asynchronous
    def options(self):
        return self.get()

    @tornado.web.asynchronous
    def connect(self):
        if os.path.isfile(CAKEY_FILE) and os.path.isfile(CACERT_FILE) and os.path.isdir(CERT_DIR):
            self.connect_intercept()
        else:
            self.connect_relay()

    def connect_intercept(self):
        """
        This function gets called when a connect request is recieved.
        * The host and port are obtained from the request uri
        * A socket is created, wrapped in ssl and then added to SSLIOStream
        * This stream is used to connect to speak to the remote host on given port
        * If the server speaks ssl on that port, callback start_tunnel is called
        * An OK response is written back to client
        * The client side socket is wrapped in ssl
        * If the wrapping is successful, a new SSLIOStream is made using that socket
        * The stream is added back to the server for monitoring
        """
        host, port = self.request.uri.split(':')

        def start_tunnel():
            try:
                self.request.connection.stream.write(b"HTTP/1.1 200 OK CONNECTION ESTABLISHED\r\n\r\n")
                wrap_socket(self.request.connection.stream.socket, host, success=ssl_success)
            #except tornado.iostream.StreamClosedError:
            except Exception:
                pass

        def ssl_success(client_socket):
            global global_httpserver
            client = tornado.iostream.SSLIOStream(client_socket)
            get_http_server().handle_stream(client, self.application.inbound_ip)  # lint:ok
            # tornado.httpserver.HTTPServer().handle_stream(client, self.application.inbound_ip)

        try:
            s = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0))
            upstream = tornado.iostream.SSLIOStream(s, ssl_options=dict(cert_reqs=ssl.CERT_NONE))
            upstream.connect((host, int(port)), start_tunnel, host)
        except Exception:
            print(("[!] Dropping CONNECT request to " + self.request.uri))
            self.write(b"404 Not Found :P")
            self.finish()

    def connect_relay(self):
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream

        def read_from_client(data):
            upstream.write(data)

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()

        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        def on_proxy_response(data=None):
            if data:
                first_line = data.splitlines()[0]
                http_v, status, text = first_line.split(None, 2)
                if int(status) == 200:
                    start_tunnel()
                    return

            self.set_status(500)
            self.finish()

        def start_proxy_tunnel():
            upstream.write('CONNECT %s HTTP/1.1\r\n' % self.request.uri)
            upstream.write('Host: %s\r\n' % self.request.uri)
            upstream.write('Proxy-Connection: Keep-Alive\r\n\r\n')
            upstream.read_until('\r\n\r\n', on_proxy_response)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(s)

        if self.application.outbound_ip and self.application.outbound_port:
            upstream.connect((self.application.outbound_ip, self.application.outbound_port), start_proxy_tunnel)
        else:
            upstream.connect((host, int(port)), start_tunnel)
