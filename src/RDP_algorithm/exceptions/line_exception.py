class LineException(Exception):

    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        return self.__message
