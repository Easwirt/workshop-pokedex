from django.db import models

from users.models import User
from pokemons.models import Pokemon


# Create your models here.
class Trade(models.Model):
    sender = models.ForeignKey(User, related_name='trades_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='trades_received', on_delete=models.CASCADE)
    pokemons_send = models.ManyToManyField(Pokemon, related_name='sent_trades')
    pokemons_received = models.ManyToManyField(Pokemon, related_name='received_trades')

