from django.db import models as m

class Museum(m.Model):
    id = m.PositiveIntegerField(primary_key=True)
    name = m.CharField(max_length=240)
    url = m.URLField(max_length=2048)
    description = m.TextField()
    access = m.BooleanField(default=False)
    address = m.CharField(max_length=440)
    district = m.CharField(max_length=40)
    tel = m.CharField(max_length=240)
    email = m.EmailField()

class Comment(m.Model):
    museum = m.ForeignKey('Museum')
    text = m.TextField()

class Added_Museum(m.Model):
    museum = m.ForeignKey('Museum')
    added = m.DateField(auto_now_add=True)

class Collection(m.Model):
    user = m.CharField(max_length=60)
    title = m.CharField(max_length=120)
    museums = m.ManyToManyField('Added_Museum')

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = 'Pagina de ' + self.user
        super().save(*args, **kwargs)
