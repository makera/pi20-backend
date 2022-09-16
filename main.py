from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape

food_kinds = [
    {
        'icon': 'lunch',
        'name': 'Dinner',
    },
    {
        'icon': 'food',
        'name': 'Breakfast',
    },
    {
        'icon': 'kitchen',
        'name': 'Lunch',
    }
]


class CustomHandler(SimpleHTTPRequestHandler):
    env = Environment(
        loader=PackageLoader("main"),
        autoescape=select_autoescape()
    )

    def do_GET(self):
        if self.path.startswith('/media/'):
            super().do_GET()
        elif self.path == '/':
            self.render_index()
        elif self.path == '/about/':
            self.render_about()

    def render_index(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        body = self.env.get_template('index.html').render(food_kinds=food_kinds)
        print(body)
        self.wfile.write(body.encode('utf-8'))


def discover_models():
    pass


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Server starting')
    httpd.serve_forever()


if __name__ == '__main__':
    run(handler_class=CustomHandler)
