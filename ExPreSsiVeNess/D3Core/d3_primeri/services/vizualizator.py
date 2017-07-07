import abc


class VizualizatorService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def naziv(self):
        pass

    @abc.abstractmethod
    def identifier(self):
        pass

    @abc.abstractmethod
    def getTree(self):
        pass

    @abc.abstractmethod
    def getHTMLContent(self):
        pass

    @abc.abstractmethod
    def getHTMLLinks(self):
        pass

    @abc.abstractmethod
    def getHTMLNodes(self):
        pass