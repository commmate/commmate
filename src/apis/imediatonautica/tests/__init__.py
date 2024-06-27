import pytest

# Monkeypatch APP_ENV to testing for unittests
mp = pytest.MonkeyPatch()
mp.setenv('APP_ENV', 'testing')
