class Response:
    @staticmethod
    def create(err=None, payload=None):
        return {
            'err': err,
            'payload': payload
        }
