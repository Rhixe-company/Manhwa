from django.db import models
from django.db.models import Q
from django.utils import timezone


class NewManager(models.QuerySet):
    def get_ongoing(self):
        return self.filter(status="Ongoing")

    def get_completed(self):
        return self.filter(status="Completed")

    def get_topcomics(self):
        not_monthly_created = ~Q(
            created_at__gt=timezone.now() - timezone.timedelta(days=31)
        ) & Q(rating__gte=10.0)

        return self.filter(not_monthly_created).order_by("-updated_at")

    def get_featuredcomics(self):
        yearly_created = ~Q(
            created_at__gt=timezone.now() - timezone.timedelta(days=186)
        ) & Q(rating__gte=10.0)
        return self.filter(yearly_created).order_by("-created_at")[6:8]
