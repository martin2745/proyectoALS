class ResenhaDto:

    def __init__(self, titulo: str, url: str, usuario: str, opinion: str):
        self._titulo = titulo
        self._url = url
        self._usuario = usuario
        self._opinion = opinion

    @property
    def titulo(self):
        return self._titulo

    @property
    def url(self):
        return self._url

    @property
    def usuario(self):
        return self._usuario

    @property
    def opinion(self):
        return self._opinion

    @staticmethod
    def find(srp: "Sirope", isbn: str, usuario: str) -> "LibroDto|None":
        return srp.find_first(ResenhaDto, lambda r: r.isbn == isbn and r.usuario == usuario)

    def __str__(self):
        t = self.titulo
        u = self.usuario
        o = self.opinion

        return f"{t}-{u}-{self._url}\n {o}"
