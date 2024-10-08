from http import HTTPStatus

from pytest import raises

from app.core.common.messages import (
    ABSTRACT_API_ERROR,
    INTERRUPT_ERROR,
    SEARCH_API_ERROR,
)
from app.core.config.scopus import API_ERRORS
from app.core.domain.exceptions import (
    ApplicationError,
    InterruptError,
    ScopusAPIError,
)
from tests.mocks.common import ANY_DICT, ERROR_RESPONSES


def test_application_error():
    with raises(ApplicationError) as error:
        raise ApplicationError(500, "any")

    assert error.value.code == 500
    assert error.value.message == "any"
    assert error.value.errors is None


def test_interrupt_error():
    with raises(InterruptError) as error:
        raise InterruptError()

    assert error.value.code == 500
    assert error.value.message == INTERRUPT_ERROR
    assert error.value.errors is None


def test_scopus_api_error_search():
    with raises(ScopusAPIError) as error:
        raise ScopusAPIError(ERROR_RESPONSES[500], SEARCH_API_ERROR)
    status = f"{500} {HTTPStatus(500).phrase}"

    assert error.value.code == 502
    assert error.value.message == SEARCH_API_ERROR
    assert error.value.errors[0]["status"] == status
    assert error.value.errors[0]["api_error"] == API_ERRORS.get(500)
    assert error.value.errors[0]["content"] == ANY_DICT


def test_scopus_api_error_abstract():
    with raises(ScopusAPIError) as error:
        raise ScopusAPIError(ERROR_RESPONSES[500], ABSTRACT_API_ERROR)
    status = f"{500} {HTTPStatus(500).phrase}"

    assert error.value.code == 502
    assert error.value.message == ABSTRACT_API_ERROR
    assert error.value.errors[0]["status"] == status
    assert error.value.errors[0]["api_error"] == API_ERRORS.get(500)
    assert error.value.errors[0]["content"] == ANY_DICT
