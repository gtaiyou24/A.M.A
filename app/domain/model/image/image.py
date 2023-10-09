from domain.model.url import URL


class Image(URL):
    def __init__(self, url: str):
        super().__init__(url)
