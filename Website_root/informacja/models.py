from django.db import models

class News(models.Model):
    img = models.ImageField(upload_to='zdjecia/', blank=True, null=True)
    header = models.CharField(max_length=40, verbose_name='Nagłówek', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    desc = models.TextField(verbose_name='Treść', blank=True, null=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Nowość'
        verbose_name_plural = 'Nowośći'

class Promotion(models.Model):
    img = models.ImageField(upload_to='zdjecia/', blank=True, null=True)
    header = models.CharField(max_length=40, verbose_name='Nagłówek', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    desc = models.TextField(verbose_name='Treść', blank=True, null=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Promocję'
        verbose_name_plural = 'Promocje'

class Humor(models.Model):
    img = models.ImageField(upload_to='zdjecia/', blank=True, null=True)
    header = models.CharField(max_length=40, verbose_name='Nagłówek', blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    desc = models.TextField(verbose_name='Treść', blank=True, null=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Ciekawą sytuację'
        verbose_name_plural = 'Sytuacje'