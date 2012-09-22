from django.forms import ModelForm, CharField, Textarea

from models import Post


class PostForm(ModelForm):
    #title = CharField(widget=Textarea(attrs))
    text = CharField(widget=Textarea(attrs={'rows': 10, 'cols': 10,
                                            'style': 'font-family: monospace'}),
    help_text='<a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html=">reStructuredText Quick Reference</a>')

    comment = CharField(help_text='Optional, used for revisions control.', required=False)

    class Meta:
        fields = ('title','text', 'tags', 'images', 'published', 'comment')
        model = Post