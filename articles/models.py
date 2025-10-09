from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.CharField(max_length=100, default="Åse Steinsland")
    source_url = models.URLField(blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("article_detail", kwargs={"slug": self.slug})
