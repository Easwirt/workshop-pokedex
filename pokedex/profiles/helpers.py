from django.utils import timezone
from datetime import timedelta

def give_daily_reward(profile):
    now = timezone.now()
    bonus_coins = 0
    if profile.last_bonus_time is None or now >= profile.last_bonus_time + timedelta(hours=24):
        profile.coins += 100
        bonus_pokemon_count = profile.pokemons.count()
        bonus_coins += bonus_pokemon_count * 3
        profile.coins += bonus_coins
        profile.last_bonus_time = now
        profile.save()
        return True, bonus_coins, None, None
    else:
        next_bonus_time = profile.last_bonus_time + timedelta(hours=24)
        remaining_time = next_bonus_time - now
        remaining_hours = remaining_time.total_seconds() // 3600
        remaining_minutes = (remaining_time.total_seconds() % 3600) // 60
        return False, bonus_coins, remaining_hours, remaining_minutes