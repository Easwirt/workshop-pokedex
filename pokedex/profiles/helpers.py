from django.utils import timezone
from datetime import timedelta

def give_daily_reward(profile):
    now = timezone.now()
    if profile.last_bonus_time is None or now >= profile.last_bonus_time + timedelta(hours=24):
        profile.coins += 100
        profile.last_bonus_time = now
        profile.save()
        return True, None, None
    else:
        next_bonus_time = profile.last_bonus_time + timedelta(hours=24)
        remaining_time = next_bonus_time - now
        remaining_hours = remaining_time.total_seconds() // 3600
        remaining_minutes = (remaining_time.total_seconds() % 3600) // 60
        return False, remaining_hours, remaining_minutes