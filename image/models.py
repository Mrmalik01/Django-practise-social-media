from django.db import models
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="images_created")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="images_liked", blank=True)
    # db_index makes query faster on that particular field (filter, order_by and exclude)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

