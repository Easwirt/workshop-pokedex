from django.db import models


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.IntegerField()
    users = models.ManyToManyField('users.User', through='UserAchievement')

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name} - {self.date_awarded}'