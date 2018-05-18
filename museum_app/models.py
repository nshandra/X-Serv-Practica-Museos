from django.db import models as m

class Comment(m.Model):
    text = m.TextField()

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
    coment = m.ManyToManyField('Comment', blank=True)

class Collection(m.Model):
    user = m.CharField(max_length=60, primary_key=True)
    title = m.CharField(max_length=120)
    css_page = m.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = 'Pagina de ' + str(self.user)
        super().save(*args, **kwargs)

class Added_Museum(m.Model):
    added = m.DateTimeField(auto_now_add=True)
    collection = m.ForeignKey('Collection')
    museum = m.ForeignKey('Museum')