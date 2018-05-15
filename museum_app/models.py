from django.db import models as m

class Comment(m.Model):
    text = m.TextField(max_length=200)

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
    coment = m.ManyToManyField('Comment')

    # def num_comments(self):
    #     num_comments = Museum.objects.coment.count()
    #     return num_comments

class Added_Museum(m.Model):
    museum = m.ForeignKey('Museum')
    added = m.DateField(auto_now_add=True)

class Collection(m.Model):
    user = m.CharField(max_length=60)
    title = m.CharField(max_length=120)
    css_page = m.TextField(default="")
    museums = m.ManyToManyField('Added_Museum')

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = 'Pagina de ' + str(self.user)
        super().save(*args, **kwargs)
