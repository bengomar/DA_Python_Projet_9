from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image


class Ticket(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=256, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (200, 200)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def __str__(self):
        return self.title


class Review(models.Model):
    objects = models.Manager()
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="rating"
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="headline")
    body = models.TextField(max_length=4096, blank=True, verbose_name="body")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket.title


class UserFollow(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )

    # def clean(self):
    #     print(self.user)
    #     print(self.followed_user)
    #     if self.user == self.followed_user:
    #         raise ValidationError("Un utilisateur ne peut pas s'abonner à lui-même.")

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
