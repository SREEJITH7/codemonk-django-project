from django.db import models
from django.conf import settings
from django.db import models

# Create your models here.

class Paragraph(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paragraphs")
    index = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "index"]),
        ]
        ordering = ["index"]

    def __str__(self):
        return f"Paragraph(user={self.user_id}, index={self.index})"


class ParagraphWordFrequency(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name="word_frequencies")
    word = models.CharField(max_length=128)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ("paragraph", "word")
        indexes = [
            models.Index(fields=["word"]),
            models.Index(fields=["paragraph", "word"]),
        ]

    def __str__(self):
        return f"{self.word}={self.count} in p#{self.paragraph_id}"


class WordFrequency(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="word_frequencies")
    word = models.CharField(max_length=128)
    total_count = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "word")
        indexes = [
            models.Index(fields=["user", "word"]),
        ]

    def __str__(self):
        return f"{self.word} total={self.total_count} for user={self.user_id}"
