from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from datetime import datetime, timedelta

from .models import Day, UpcomingDate

@receiver(post_save, sender=Day)
def create_upcoming_dates(sender, instance, created, **kwargs):
    if created:
        for i in range(0, 365, 7):
            date = datetime.now() + timedelta(days=i)
            day = instance
            UpcomingDate.objects.create(date=date, day=day)
            print(f"Upcoming date {date} created for {day}")