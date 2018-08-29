# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin
from django_admin_related import utils as u
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
import json


class VerifyRelated(ModelAdmin):
    # remove original bulk delete (this no verify related before related)
    def get_actions(self, request):
        actions = super(VerifyRelated, self).get_actions(request)
        
        if 'delete_selected' in actions:
            del actions['delete_selected']

        # Append new delete selected action
        actions['bulk_delete'] = (u.bulk_delete, 'bulk_delete', u.bulk_delete.short_description)
        
        return actions

    # internal delete 
    def delete_model(self, request, obj):
        if not u.delete_model(self, request, obj):
            super(VerifyRelated, self).delete_model(request, obj)

    # internal delete response (removed messages)
    def response_delete(self, request, obj_display, obj_id):
        """
        Determine the HttpResponse for the delete_view stage.
        """
        opts = self.model._meta

        if '_popup' in request.POST:
            popup_response_data = json.dumps({
                'action': 'delete',
                'value': str(obj_id),
            })
            return TemplateResponse(request, self.popup_response_template or [
                'admin/%s/%s/popup_response.html' % (opts.app_label, opts.model_name),
                'admin/%s/popup_response.html' % opts.app_label,
                'admin/popup_response.html',
            ], {
                'popup_response_data': popup_response_data,
            })


        if self.has_change_permission(request, None):
            post_url = reverse(
                'admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, post_url
            )
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)

        return HttpResponseRedirect(post_url)