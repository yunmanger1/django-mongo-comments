#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from c0mments.models import C0MMENT_MAX_LENGTH, Comment
from django.utils.translation import ugettext as _


class CommentForm(forms.Form):
    parent = forms.CharField(widget=forms.HiddenInput, required=False, max_length=30)
    comment = forms.CharField(label=_('Comment'),
        max_length=C0MMENT_MAX_LENGTH,
        widget=forms.Textarea(attrs={'placeholder': _('Type your comment here')}))

    def clean_parent(self):
        parent = self.cleaned_data.get('parent', None)
        if parent:
            try:
                return Comment.objects.get(pk=parent)
            except Comment.DoesNotExist:
                raise forms.ValidationError(_('Replied comment is not found.'))
        return None
