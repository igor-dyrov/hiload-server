import datetime

from http_constants import STATUS_CODES, SERVER


class Response:
    def __init__(self, http_version, status_code, content_length=None, content_type=None, data=None):
        self.http_version = http_version
        self.status_code = status_code
        self.reason_phrase = STATUS_CODES[status_code]
        self.content_length = content_length
        self.content_type = content_type
        self.data = data

    def __get_starting_line(self):
        return "%s %d %s\r\n" % (self.http_version, int(self.status_code), self.reason_phrase)

    @staticmethod
    def __get_server():
        return "Server: " + SERVER + "\r\n"

    @staticmethod
    def __get_date():
        date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        return "Date: " + date + "\r\n"

    def __get_content_length(self):
        return "Content-Length: " + str(self.content_length) + "\r\n"

    def __get_content_type(self):
        return "Content-Type: " + self.content_type + "\r\n"

    def __get_data(self):
        return self.data

    def __bytes__(self):
        resp_string = self.__get_starting_line() + self.__get_server() + self.__get_date()
        if self.content_length is not None:
            resp_string += self.__get_content_length()
        if self.content_type is not None:
            resp_string += self.__get_content_type()
        resp_string += '\r\n'
        resp_string = resp_string.encode('utf-8')
        if self.data is not None:
            resp_string += self.__get_data()

        return resp_string
