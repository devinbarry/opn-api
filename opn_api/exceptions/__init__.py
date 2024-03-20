class ParsingError(Exception):
    def __init__(self, uuid, element, msg):
        self.uuid = uuid
        self.element = element
        super().__init__(msg)
