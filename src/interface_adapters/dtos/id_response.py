from interface_adapters.interfaces.id import Id

class IdResponse(Id):

    def __init__(self, id: str) -> None:
        self.id: str = id
