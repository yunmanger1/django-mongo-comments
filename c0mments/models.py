import mongoengine as mg
from django.conf import settings
from django.utils.importlib import import_module
from django.utils import timezone
C0MMENT_USER_DOCUMENT = getattr(settings, 'C0MMENT_USER_DOCUMENT', 'mongoengine.django.auth.User')
C0MMENT_MAX_LENGTH = getattr(settings, 'C0MMENT_MAX_LENGTH', 3000)
PUBIC_COMMENT, NOT_PUBLIC_COMMENT, REMOVED_COMMENT = range(3)


def get_user_document(path):
    tmp = path.split('.')
    module_str, document_str = ".".join(tmp[:-1]), tmp[-1]
    module = import_module(module_str)
    return getattr(module, document_str)

User = get_user_document(C0MMENT_USER_DOCUMENT)


class CommentQuerySet(mg.queryset.QuerySet):

    def for_object(self, obj):
        return self.__call__(content_object=obj)


class Comment(mg.Document):
    user = mg.ReferenceField(User, required=True)
    parent = mg.ReferenceField('self', required=False)
    comment = mg.StringField(required=True)
    submit_date = mg.DateTimeField()
    status = mg.IntField(required=True, default=PUBIC_COMMENT)
    content_object = mg.GenericReferenceField()

    meta = {
        'allow_inheritance': True,
        'ordering': ('submit_date',),
        'queryset_class': CommentQuerySet,
    }

    def save(self, *a, **kw):
        if self.submit_date is None:
            self.submit_date = timezone.now()
        super(Comment, self).save(*a, **kw)
