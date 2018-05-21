from django import forms
from museum_app.models import Comment, Added_Museum, Collection
from django.utils.translation import ugettext_lazy as _


class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 1, 'cols': 30,
                                                 'placeholder': _('comment')})}

    # remove label
    def __init__(self, *args, **kwargs):
        super(Comment_Form, self).__init__(*args, **kwargs)
        self.fields['text'].label = False


class CSS_Form(forms.ModelForm):
    f = forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 30})
    css_page = forms.CharField(required=False, widget=f)

    class Meta:
        model = Collection
        fields = ['css_page']

    # remove label
    def __init__(self, *args, **kwargs):
        super(CSS_Form, self).__init__(*args, **kwargs)
        self.fields['css_page'].label = False


class Title_Form(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title']
        widgets = {'title': forms.Textarea(attrs={'class': 'form-control',
                                                  'rows': 1, 'cols': 30})}

    # remove label
    def __init__(self, *args, **kwargs):
        super(Title_Form, self).__init__(*args, **kwargs)
        self.fields['title'].label = False
