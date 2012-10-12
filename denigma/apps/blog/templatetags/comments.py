from django import template

from blog.models import Post, Comment


register = template.Library()

@register.inclusion_tag('blog/comments.html')
def display_comments(post_id):
    post = Post.objects.get(id__exact=post_id)
    comments = Comment.objects.filter(post=post)[0:5]
    return {'comments': comments}
 
