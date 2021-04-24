from django.db import models


class Follow(models.Model):
    # User(username=admin, follows=[admin->dag], followers=[])
    follower = models.ForeignKey( # Кто подписался
        'auth.User', related_name='follows', on_delete=models.CASCADE
    )
    # User(username=admin, follows=[], followers=[admin->dag])
    follows = models.ForeignKey( # На кого подписался
        'auth.User', related_name='followers', on_delete=models.CASCADE
    )
    followed = models.DateTimeField(auto_now_add=True) # Когда подписался

    def __str__(self):
        return f"{self.follower} -> {self.follows}"


class Tweet(models.Model):
    text = models.CharField(max_length=240, verbose_name='Текст')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')
    created = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    photo = models.URLField(verbose_name='Фото', max_length=200, blank=True)

    class Meta:
        verbose_name_plural = 'Твиты'
        verbose_name = 'Твит'
        ordering = ['-created']

    def __str__(self):
        return f"[{self.author.username}] {self.text}"
