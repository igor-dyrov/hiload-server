from urllib.parse import unquote


class Request:
    def __init__(self, raw_request):
        self.request = raw_request.decode('utf-8')
        listed_request = self.request.split(' ')
        if len(listed_request) < 3:
            self.valid = False
        else:
            self.method = listed_request[0]
            path = unquote(listed_request[1])
            self.path = path.split('?')[0]
            self.valid = True

    def __repr__(self):
        return self.request
