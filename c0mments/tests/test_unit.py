import mongoengine as mg
from c0mments import models as md
from c0mments.utils.test import use_tdb


@use_tdb
def test_get_user_document():
    ''' test import user document '''
    User = md.get_user_document('mongoengine.django.auth.User')
    assert User.__name__ == 'User'


@use_tdb
def test_add_comment():
    ''' test adding comment '''
    class Post(mg.Document):
        pass
    post = Post.objects.create()
    assert post.pk is not None
    user = md.User.create_user('test', 'test')
    comment = md.Comment.objects.create(content_object=post, comment='asdf', user=user)
    assert comment.pk is not None
    assert md.Comment.objects.for_object(post).count() == 1
