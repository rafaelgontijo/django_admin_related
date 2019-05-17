from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from django.contrib import messages
from django.contrib.admin.actions import delete_selected
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import ugettext_lazy as _


# Verify related
def has_related(modeladmin, obj):
    if not hasattr(modeladmin, 'verify_related_fields'):
        fields = obj._meta.get_fields(include_hidden=False)
    else:
        fields = []
        for field in modeladmin.verify_related_fields:
            try:
                fields.append(obj._meta.get_field(field))
            except FieldDoesNotExist:
                pass

    for rel in fields:
        try:
            # check if there is a relationship with at least one related object
            related = rel.related_model.objects.filter(**{rel.field.name: obj})
            if related.exists():
                # if there is return a Tuple of flag = False the related_model object
                return True
        except AttributeError:  # an attribute error for field occurs when checking for AutoField
            pass  # just pass as we dont need to check for AutoField

    return False


# Bulk delete, (dropdown, in django admin list objects)
def bulk_delete(modeladmin, request, queryset):

    for obj in queryset.all():
        if has_related(modeladmin, obj):
            messages.error(request, _('One or more selected items, contains linked templates, can not be deleted.'))
            return

    return delete_selected(modeladmin, request, queryset)

bulk_delete.allowed_permissions = ('delete',)   
bulk_delete.short_description = _("Delete selected %(verbose_name_plural)s")


# Delete internal
def delete_model(self, request, obj):
    related = has_related(self, obj)
    
    if related:
        messages.error(request, _('This item contains linked models, could not be deleted.'))
    else:
        messages.success(request, _("Successfully deleted."))
        
    return related