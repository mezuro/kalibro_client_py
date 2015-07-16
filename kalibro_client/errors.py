class KalibroClientError(RuntimeError):
    pass

class KalibroClientSaveError(KalibroClientError):
    pass

class KalibroClientDeleteError(KalibroClientError):
    pass

class KalibroClientNotFoundError(KalibroClientError):
    pass
