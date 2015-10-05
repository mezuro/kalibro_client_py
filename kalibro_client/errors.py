class KalibroClientError(RuntimeError):
    pass

class KalibroClientRequestError(KalibroClientError):
    def __init__(self, response, *args, **kwargs):
        super(KalibroClientRequestError, self).__init__(response.json().get('errors', None),
            *args, **kwargs)
        self._response = response

    @property
    def response(self):
        return self._response

class KalibroClientSaveError(KalibroClientError):
    pass

class KalibroClientDeleteError(KalibroClientError):
    pass

class KalibroClientNotFoundError(KalibroClientError):
    pass
