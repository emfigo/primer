import pytest

from primer import app, db


@pytest.fixture(scope='session')
def database(request):
    db.create_all()

    yield db

    @request.addfinalizer
    def drop_database():
        db.session.remove()
        db.drop_all()
