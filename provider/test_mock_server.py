from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import signal
import jwt

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port

class MockAAuthServerRequestHandler(BaseHTTPRequestHandler):
    LOGIN_PATTERN = re.compile(r'/auth/login')
    def do_POST(self):
        if re.search(self.LOGIN_PATTERN, self.path):
            
            token_data = {
                'identity': {'username':'test1', 'userid':'8888888888', 'roles':{}}
            }
            access_token = jwt.encode(token_data, 'test123', 'HS256').decode('utf-8')
            
            self.send_response(requests.codes.ok)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            self.wfile.write(json.dumps({'access_token': access_token}).encode())
        return

def start_mock_auth_server():
    mock_server_port = get_free_port()
    mock_server = HTTPServer(('localhost', mock_server_port), MockAAuthServerRequestHandler)
    def service_shutdown(signal_number, frame):
        self.mock_server.shutdown()
        sys.exit(0)
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    # Start running mock server in a separate thread.
    # Daemon threads automatically shut down when the main process exits.
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()

if __name__ == '__main__':
    start_mock_auth_server()

