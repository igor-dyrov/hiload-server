from server import Server
from config import Config

CONFIG_PATH = 'httpd.conf'

if __name__ == '__main__':
    config = Config(CONFIG_PATH)

    server = Server(4, '', config.address_port, config.receive_data_size, config.queue)
    server.start()
    