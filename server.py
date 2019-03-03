import os
import socket

from http_constants import StatusCode, ALLOWED_METHODS, CONTENT_TYPES, HTTP_VERSION
from logger import Logger
from request import Request
from response import Response
from config import Config

logger = Logger().logger


class Server:
    def __init__(self, ncpu, root, address_port, receive_data_size, queue):
        self.ncpu = ncpu
        self.root = root
        self.address_port = address_port
        self.receive_data_size = receive_data_size
        self.queue = queue
        self.workers = []

    @staticmethod
    def __get_content_type(filepath):
        extension = filepath.split('.')[-1]
        content_type = CONTENT_TYPES.get(extension)
        return content_type

    def __handle_request(self, request):
        if request.method not in ALLOWED_METHODS:
            return Response(HTTP_VERSION, StatusCode.METHOD_NOT_ALLOWED)

        filepath = self.root + request.path
        filepath = os.path.normpath(filepath)
        filepath = '/server/' + filepath
        logger.info(filepath)
        if not os.path.exists(filepath):
            return Response(HTTP_VERSION, StatusCode.NOT_FOUND)
        if os.path.isdir(filepath):
            filepath += '/index.html'
        if not os.path.exists(filepath):
            return Response(HTTP_VERSION, StatusCode.FORBIDDEN)
        if not os.path.isfile(filepath):
            return Response(HTTP_VERSION, StatusCode.FORBIDDEN)

        data = content_type = None
        content_length = 0

        try:
            with open(filepath, 'rb') as file:
                data = file.read()
                content_length = len(data)
                content_type = self.__get_content_type(filepath)
        except Exception as e:
            logger.info('Error in reading file:\n %s' % e)

        if content_type is None:
            return Response(HTTP_VERSION, StatusCode.NOT_FOUND)

        if request.method == 'HEAD':
            return Response(HTTP_VERSION, StatusCode.OK, content_length, content_type)

        return Response(HTTP_VERSION, StatusCode.OK, content_length, content_type, data)

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(self.address_port)
        server_socket.listen(self.queue)

        logger.info('Listening on %s:%d...' % self.address_port)
        logger.info('Number of the processes: %d' % self.ncpu)
        logger.info('Files root: %s' % self.root)

        for worker in range(self.ncpu):
            pid = os.fork()
            if pid > 0:
                self.workers.append(pid)
            elif pid == 0:
                logger.info('Created worker with pid: %d' % os.getpid())
                while True:
                    client_socket, client_address = server_socket.accept()
                    raw_request = client_socket.recv(self.receive_data_size)

                    if raw_request.strip() == 0:
                        client_socket.close()
                        continue

                    request = Request(raw_request)
                    if not request.valid:
                        response = Response(HTTP_VERSION, StatusCode.FORBIDDEN)
                    else:
                        response = self.__handle_request(request)
                    client_socket.send(bytes(response))
                    client_socket.close()
            else:
                logger.info("Couldn't fork")

        server_socket.close()

        for worker_pid in self.workers:
            os.waitpid(worker_pid, 0)


if __name__ == '__main__':
    config = Config()
    server = Server(config.cpu_number, config.root, config.address_port, config.receive_data_size, config.queue)
    server.start()
