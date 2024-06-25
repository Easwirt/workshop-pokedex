from django.db import models
from profiles.models import Profile
from asgiref.sync import sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver

class Boss(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='minigame/bosses/')
    health = models.IntegerField(default=100)
    health_regen = models.IntegerField(default=100)
    duration = models.IntegerField(default=120)
    difficulty = models.CharField(max_length=50, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    story = models.TextField(blank=True, null=True)
    reward = models.IntegerField(default=100)
    defeat_penalty = models.IntegerField(default=10)
    defeat_text = models.TextField(blank=True, null=True)
    victory_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Fight(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE)
    status = models.IntegerField(default=1) # 1 - game, 0 - lose, 2 - victory
    max_health = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    health_regen = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    fight_done = models.BooleanField(default=False)
    attack_damage = models.IntegerField(default=0)


    async def victory(self):
        if not self.fight_done:
            profile = await sync_to_async(lambda: self.profile)()
            boss = await sync_to_async(lambda: self.boss)()

            if profile and boss:
                profile.boss += 1
                profile.coins += boss.reward
                await sync_to_async(lambda: profile.save())()
                self.fight_done = True


    async def lose(self):
        if not self.fight_done:
            profile = await sync_to_async(lambda: self.profile)()
            boss = await sync_to_async(lambda: self.boss)()

            if profile and boss:
                profile.coins -= self.boss.defeat_penalty
                await sync_to_async(lambda: profile.save())()
                self.fight_done = True

    def __str__(self):
        return f'{self.profile.user.username} vs {self.boss.name}'
    
    class Meta:
        verbose_name = 'Fight'
        verbose_name_plural = 'Fights'


@receiver(post_save, sender=Fight)
def fight_activate(sender, instance, created, **kwargs):

    if created:
        instance.health = instance.boss.health
        instance.time = instance.boss.duration
        instance.max_health = instance.boss.health
        instance.health_regen = instance.boss.health_regen
        instance.attack_damage = instance.profile.attack_damage + 1
        instance.save()