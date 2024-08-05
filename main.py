import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from user import User
from repository import InMemoryUserRepository, DatabaseUserRepository

class Config:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.repo_type = config['repo_type']
        self.db_url = config.get('db_url')

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, user_data):
        user = User(**user_data)
        self.repository.add_user(user)

    def update_user(self, iduser, user_data):
        user = self.repository.get_user(iduser)
        if user:
            user.lastname = user_data.get('lastname', user.lastname)
            user.firstname = user_data.get('firstname', user.firstname)
            user.middlename = user_data.get('middlename', user.middlename)
            self.repository.edit_user(user)
            return user
        return None

    def get_user(self, iduser):
        return self.repository.get_user(iduser)

    def delete_user(self, iduser):
        self.repository.delete_user(iduser)

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/user':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user_data = json.loads(post_data)
            user_service.create_user(user_data)
            self.send_response(201)
            self.end_headers()

    def do_PUT(self):
        if self.path.startswith('/user/'):
            iduser = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user_data = json.loads(post_data)
            user = user_service.update_user(iduser, user_data)
            if user:
                self.send_response(200)
            else:
                self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path.startswith('/user/'):
            iduser = int(self.path.split('/')[-1])
            user = user_service.get_user(iduser)
            if user:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(user.to_dict()).encode())
            else:
                self.send_response(404)
                self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/user/'):
            iduser = int(self.path.split('/')[-1])
            user_service.delete_user(iduser)
            self.send_response(204)
            self.end_headers()

if __name__ == "__main__":
    config = Config('config.json')
    if config.repo_type == 'in_memory':
        repository = InMemoryUserRepository()
    elif config.repo_type == 'database':
        repository = DatabaseUserRepository(config.db_url)
    else:
        raise ValueError('Invalid repository type')

    user_service = UserService(repository)

    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Starting server at http://localhost:8000")
    server.serve_forever()
