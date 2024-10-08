from fastapi import Request
from pandas import read_csv

from app.core.common.types import Context, Table
from app.core.config.config import FILE_PATH, FILENAME, TOKEN, TOML_ENV
from app.core.domain.metaclasses import TemplateContext


class TemplateContextBuilder(TemplateContext):
    """Generates context values for template responses"""

    __WEB_APP_URL = "/scopus-survey/api"
    __INDEX_HTML = "index.html"
    __TABLE_HTML = "table.html"
    __ENCODING = "utf-8"
    __SEP = ";"
    __WEB_APP_DATA = {
        "token": TOKEN,
        "filename": FILENAME,
        "table_url": "/scopus-survey/api/table",
        "search_url": "/scopus-survey/api/search-articles",
        "description": TOML_ENV.description,
    }

    def __init__(self, request: Request) -> None:
        """Generates context values for template responses"""
        self.__request = request
        self.__data = {
            "request": request,
            "version": TOML_ENV.version,
            "repository": TOML_ENV.repository,
            "swagger_url": "/",
        }

    def get_web_app_context(self) -> Context:
        self.__data.update(self.__WEB_APP_DATA)
        return self.__request, self.__INDEX_HTML, self.__data

    def get_table_context(self) -> Context:
        self.__data.setdefault("content", self.__get_table())
        self.__data.setdefault("web_app_url", self.__WEB_APP_URL)
        return self.__request, self.__TABLE_HTML, self.__data

    def __get_table(self) -> Table:
        try:
            data = read_csv(
                FILE_PATH, sep=self.__SEP, encoding=self.__ENCODING
            )
            return data.to_numpy().tolist()
        except FileNotFoundError:
            return None
