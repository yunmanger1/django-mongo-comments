#!/usr/bin/python
# -*- coding: utf-8 -*-

# from c0mments.models import Comment
# from mongotools.forms import MongoForm

from django.views.generic.edit import FormMixin
from c0mments.forms import CommentForm
from c0mments.models import Comment
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
import simplejson


def annotate_comments(queryset):
    used = set()
    comments = list(queryset.order_by('submit_date'))
    result = []

    def fetch_children(parent, depth=0):
        # global result
        # global comments
        for comment in comments:
            if comment.parent == parent and comment.pk not in used:
                comment.indent = depth * 20
                result.append(comment)
                used.add(comment.pk)
                fetch_children(comment, depth + 1)

    fetch_children(None, 0)
    return result


class CommentCreateView(FormMixin):

    form_class = CommentForm

    def get_object_comments(self, object):
        return annotate_comments(Comment.objects.for_object(object))

    def form_valid(self, form):
        comment = form.cleaned_data.get('comment')
        parent = form.cleaned_data.get('parent', None)
        content = self.get_object()
        self.success_url = self.request.path
        comment = Comment.objects.create(content_object=content,
                comment=comment, parent=parent, user=self.request.user)
        if self.request.is_ajax():
            data = {'message': _('Comment was successfully added'),
                    'comment': render_to_string('c0mments/comment.html',
                        {'object': comment})}
            return self.json_response(data)
        return super(CommentCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            print form.errors
            return self.json_response({'error': True, 'message': u'Ошибка'})
        return self.get(self.request, *self.args, **self.kwargs)

    def get_context_data(self, **kw):
        ctx = super(CommentCreateView, self).get_context_data(**kw)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ctx.update({'form': form,
                   'comments': self.get_object_comments(self.get_object())})
        return ctx

    def post(
        self,
        request,
        *args,
        **kwargs
        ):

        if not request.user.is_authenticated():
            return redirect_to_login(request.path)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def json_response(self, data, status_code=200):
        return HttpResponse(simplejson.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            status=status_code)
