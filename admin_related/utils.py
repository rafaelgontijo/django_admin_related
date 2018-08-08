from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from django.contrib import messages
from django.contrib.admin.actions import delete_selected
from django.utils.translation import gettext_lazy as _


# Verify related
def has_related(obj):
    for field in obj._meta.get_fields(include_hidden=False):
        
        if field.name != 'id' and isinstance(field, (ManyToOneRel, ManyToManyRel)):
            objects = getattr(obj, field.name+'_set').all().first()
            
            if objects:
                return True

    return False


# Bulk delete, (dropdown, in django admin list objects)
def bulk_delete(self, request, queryset):
    for obj in queryset.all():
        if has_related(obj):
            messages.error(request, 'One or more selected items, contains linked templates, can not be deleted.')
        
        else:
            request.POST._mutable=True
            request.POST['action'] = 'bulk_delete'
            request.POST._mutable=False
            return delete_selected(self, request, queryset)

bulk_delete.allowed_permissions = ('delete',)   
bulk_delete.short_description = _("Delete selected %(verbose_name_plural)s")


# Delete internal
def delete_model(self, request, obj):
    related = has_related(obj)
    
    if related:
        messages.error(request, _('This item contains linked models, could not be deleted.'))
    else:
        messages.success(request, _("Successfully deleted."))
    return related