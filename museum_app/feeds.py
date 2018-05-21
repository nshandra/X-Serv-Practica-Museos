from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from museum_app.models import Museum, Comment
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _


class top_museums_feed(Feed):
    title = _("Most commented museums")
    link = "/topmuseums"
    description = _("List top five museums by number of comments.")

    def items(self):
        return Museum.objects.exclude(coment__isnull=True)\
            .annotate(num_coment=Count('coment'))\
            .order_by('-num_coment')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('museum', args=(item.id,))


class last_comment_feed(Feed):
    title = _("Last comments")
    link = "/lastcomments"
    description = _("List five last comments.")

    def items(self):
        return Comment.objects.all().order_by('-id')[:5]

    def item_title(self, item):
        return Museum.objects.get(coment=item.id).name

    def item_description(self, item):
        return item.text

    def item_link(self, item):
        id = Museum.objects.get(coment=item.id).id
        return reverse('museum', args=(id,))
