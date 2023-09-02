from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from PIL import Image


class Ticket(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=256, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    # IMAGE_MAX_SIZE = (800, 800)
    #
    # def resize_image(self):
    #     image = Image.open(self.image)
    #     image.thumbnail(self.IMAGE_MAX_SIZE)
    #     image.save(self.image.path)
    #
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.resize_image()


class Review(models.Model):
    objects = models.Manager()
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                          MaxValueValidator(5)],
                                              verbose_name='rating'
                                              )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name='headline')
    body = models.TextField(max_length=4096, blank=True, verbose_name='body')
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='followed_by')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user', )
