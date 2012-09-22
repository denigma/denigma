from django import forms

class ArticleForm(ModelForm):
    pub_date = forms.DateField(label='Publication date')