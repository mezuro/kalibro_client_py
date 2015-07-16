class KalibroClientError(RuntimeError):
    pass

class KalibroClientSaveError(KalibroClientError):
    pass

class KalibroClientNotFoundError(KalibroClientError):
    pass
