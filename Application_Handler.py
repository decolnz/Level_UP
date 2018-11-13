import logging
import http.server
import urllib.parse
import Database as Db

footer = '</body></html>'


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        with open('HTML/Header.html') as page_header:
            header = page_header.read()

        network = urllib.parse.urlparse(self.path)

        if network.path == '/':
            with open('HTML/Mainpage.html') as main_page:
                index = main_page.read()
                content = header + index + footer

            content_type = 'text/html; charset=utf-8'
            response_code = 200

        elif network.path == '/login':
            with open('HTML/Login.html', 'rb') as login:
                login_form = login.read().decode('UTF-8')
                content = header + login_form + footer

            content_type = 'text/html; charset=utf-8'
            response_code = 200

        # elif network.path == '/login_user':
        #     params_dict = urllib.parse.parse_qs(network.query)
        #     username = str(params_dict['username'][0])
        #     password = str(params_dict['password'][0])
        #     cache = Db.login(self.base.connect(), username, password)
        #     network.path = f'/home/{cache}'
        #
        #     content = header + footer
        #     content_type = 'text/html; charset=utf-8'
        #     response_code = 200

        else:
            content = 'Unknown path'
            content_type = 'text/html; charset=utf-8'
            response_code = 401

        return self.respond(response_code, content_type, content)

    def do_POST(self):
        with open('HTML/Header.html') as page_header:
            header = page_header.read()

        network = urllib.parse.urlparse(self.path)

        if network.path == '/login_user':
            params_dict = urllib.parse.parse_qs(network.query)
            username = str(params_dict['username'][0])
            password = str(params_dict['password'][0])
            cache = Db.login(self.base.connect(), username, password)
            network.path = f'/home/{cache}'

            content = header + footer
            content_type = 'text/html; charset=utf-8'
            response_code = 200

        else:
            content = 'Unknown path'
            content_type = 'text/html; charset=utf-8'
            response_code = 401

        return self.respond(response_code, content_type, content)

    def respond(self, _status_code, _content_type, _content):
        self.send_response(_status_code)
        self.send_header('Content-type', _content_type)
        self.end_headers()

        if isinstance(_content, str):
            _content = bytearray(_content, 'UTF-8')

        self.wfile.write(_content)


HOST_NAME = 'localhost'
PORT_NUMBER = 8080
logging.basicConfig(level=logging.INFO)

httpd = http.server.HTTPServer((HOST_NAME, PORT_NUMBER), Handler)
Handler.base = Db.register_database()

logging.info(f'Server Started - {HOST_NAME}:{PORT_NUMBER}')

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
logging.info(f'Server Stopped - {HOST_NAME}:{PORT_NUMBER}')
