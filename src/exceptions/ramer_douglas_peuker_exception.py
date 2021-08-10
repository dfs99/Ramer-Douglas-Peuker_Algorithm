class RDPException(Exception):

    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return self.message


class RDPPainterException(Exception):

    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        return self.__message

    def __str__(self):
        return self.message
