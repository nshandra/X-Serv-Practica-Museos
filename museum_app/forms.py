from django import forms
from museum_app.models import Museum, Comment

class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'