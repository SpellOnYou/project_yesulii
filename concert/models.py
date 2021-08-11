from django.db import models

class ConcertList(models.Model):
    title = models.CharField(max_length=200, help_text='제목')
    date = models.DateField(help_text='일자')
    time = models.TimeField(blank=True, null=True, help_text='시간')
    link = models.URLField(help_text='링크')
    place = models.CharField(max_length=200, help_text='장소')

    class Meta:
        ordering = ['date']
        
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    