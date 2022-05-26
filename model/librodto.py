class LibroDto:

    def __init__(self, titulo: str, autor: str, isbn: str, url: str, argumento: str):
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._url = url
        self._argumento = argumento
        self.__modificado = False

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, v):
        self._titulo = v

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, v):
        self._autor = v

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, v):
        self._isbn = v

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, v):
        self._url = v

    @property
    def argumento(self):
        return self._argumento

    @argumento.setter
    def argumento(self, v):
        self._argumento = v

    @staticmethod
    def find(srp: "Sirope", isbn: str) -> "LibroDto|None":
        return srp.find_first(LibroDto, lambda l: l.isbn == isbn)

    def __str__(self):
        t = self.titulo
        a = self.autor
        isbn = self.isbn
        arg = self.argumento

        return f"{t} ({a})-{isbn}\n {arg}"
