from django.db import models
import datetime

# Create your models here.

NEWS_TYPE_CHOICES = [("Positive","Positive"), ("Negative", "Negative"), ("Neutral", "Neutral")]

class News(models.Model):
    title = models.CharField(max_length=1023)
    description = models.TextField()
    news_type = models.CharField(choices=NEWS_TYPE_CHOICES, max_length=16)
    isPublished = models.BooleanField(default=False, blank=True)
    publish_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def publish(self):
        if not self.isPublished:
            self.isPublished = True
            self.publish_time = datetime.datetime.now()
            self.save()

    @staticmethod
    def getPublishedNews():
        queryset = News.objects.filter(isPublished = True).order_by('-publish_time')
        return queryset
        
