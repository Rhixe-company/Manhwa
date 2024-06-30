import pytest
from core.factories import ComicFactory


@pytest.fixture
def comics():
    return ComicFactory.create_batch(4)
