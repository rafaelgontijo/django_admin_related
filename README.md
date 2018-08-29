Django Admin Related
====================

# Install:
    pip install django-admin-related

# Usage:

1. Add to your INSTALLED_APPS, in settings.py:

        INSTALLED_APPS = [  
            ...
            'django_admin_related',
            ...
        ]  

2. Create admin for your model:

        from django.contrib.admin import register
        from django_admin_related.admin import VerifyRelated

        @register(YouModel)
        class YouModelAdmin(VerifyRelated):
            pass

3. Test:

        try this: create a simple model, and simple related model, and exclude a first model.

# Advanced:

1. if you need to specify relationships, you can do so :

        from django.contrib.admin import register
        from django_admin_related.admin import VerifyRelated

        @register(YouModel)
        class YouModelAdmin(VerifyRelated):
            verify_related_fields = ('field', 'field2', ...)
