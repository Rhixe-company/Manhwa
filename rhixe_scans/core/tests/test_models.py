import pytest
from core.models import Comic


@pytest.mark.django_db
def test_queryset_get_ongoing_method(comics):
    qs = Comic.objects.get_ongoing()
    assert qs.count() > 0
    assert all([comics.status == "Ongoing" for comics in qs])


@pytest.mark.django_db
def test_queryset_get_completed_method(comics):
    qs = Comic.objects.get_completed()
    assert qs.count() > 0
    assert all([comics.status == "Completed" for comics in qs])
