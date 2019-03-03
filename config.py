import os
import re


class Config:
    ADDRESS = '0.0.0.0'
    PORT = 80
    QUEUE = 8
    RECEIVE_DATA_SIZE = 1024

    def __init__(self, config_path):
        self.config_path = '/server/httpd.conf'
        self.cpu_number = self.root = None
        if not os.path.exists(self.config_path):
            raise ValueError('No config file at path: %s' % self.config_path)
        else:
            try:
                with open(self.config_path, 'r') as file:
                    data = file.read()
                    kv = data.split('\n')
                    options = {}
                    for v in kv:
                        if v:
                            (key, value) = re.search(r'\S* \S*', v).group(0).split(' ')
                            options[key] = value
                    self.address_port = (self.ADDRESS, self.PORT)
                    self.queue = self.QUEUE
                    self.receive_data_size = self.RECEIVE_DATA_SIZE
            except Exception as e:
                raise ValueError('Error in reading file:\n %s' % e)
