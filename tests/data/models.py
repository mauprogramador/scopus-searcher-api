from json import dumps, loads

from pydantic import BaseModel, Field


class Request:
    def __init__(self, token: str | None = None):
        self.headers = {'X-Access-Token': token}


class FakeResponse:
    def __init__(self, content: dict | str = None, status_code: int = None):
        if content or (isinstance(content, str) and len(content) == 0):
            self.text = content if isinstance(content, str) else dumps(content)
        self.status_code = status_code or 200
        self.body = 'any'.encode()

    def json(self) -> dict:
        return loads(self.text)


class Article(BaseModel):
    link: str = Field(serialization_alias='@_fa', default='true')
    url: str = Field(serialization_alias='prism:url', default='any')
    volume: str = Field(serialization_alias='prism:volume', default='any')
    date: str = Field(serialization_alias='prism:coverDate', default='any')
    doi: str = Field(serialization_alias='prism:doi', default='any')
    citations: str = Field(serialization_alias='citedby-count', default='any')
    title: str = Field(serialization_alias='dc:title', default='any')
    scopus_id: str = Field(
        serialization_alias='dc:identifier', default='SCOPUS_ID:12345'
    )
    publication_name: str = Field(
        serialization_alias='prism:publicationName', default='any'
    )
