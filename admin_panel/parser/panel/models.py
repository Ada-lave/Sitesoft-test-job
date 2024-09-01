from django.db import models

class Hab(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя хаба")
    link = models.TextField(verbose_name="Ссылка до главной страницы хаба")
    interval = models.IntegerField(verbose_name="Интервал работы")
    
    class Meta:
        db_table = "habs"
    

class Article(models.Model):
    heading = models.CharField(max_length=200, verbose_name="Заголовок публикации")
    link = models.TextField(verbose_name="Ссылка до публикации")
    author_name = models.CharField(max_length=200, verbose_name="Имя автора")
    author_link = models.CharField(max_length=200, verbose_name="Ссылка до автора")
    published_at = models.DateTimeField(verbose_name="Время публикации")
    hab = models.ForeignKey(Hab, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "articles"
