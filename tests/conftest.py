import pytest


@pytest.fixture(scope="module")
def script_loc(request):
    """Return the directory of the currently running test script"""

    return request.path.parent


@pytest.fixture(scope='session')
def tmpdir_session(request, tmp_path_factory):
    """A tmpdir fixture for the session scope. Persists throughout the pytest session."""

    return tmp_path_factory.mktemp(tmp_path_factory.getbasetemp().name)
