from klausurensammlung.models import Schlagwort, Stufe, MCFrage, StandardFrage, Fach, Reihe
from django.contrib import admin
from django.db import models
from django_select2.widgets import Select2MultipleWidget

import datetime

admin.site.register(Schlagwort)
admin.site.register(Stufe)
admin.site.register(Fach)
admin.site.register(Reihe)

class UserAccessInfo (admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
            obj.created = datetime.datetime.now().date()

        obj.lastEditor = request.user
        obj.edited = datetime.datetime.now().date()

        obj.save()

    def has_permissions (self,request, obj=None):
        print "has permissions", obj, request.user
        return True
    
    def has_change_permission(self, request, obj=None):
        # r = self.has_permissions(request, obj)
        print "has change permission"
        if obj:
            if (obj.creator == request.user or
                request.user.is_superuser):
                return True
            else:
                return False
        else:
            return True


    def has_delete_permission(self, request, obj=None):
        # r=self.has_permissions(request, obj)
        print "has delerte permission"
        if obj:
            if (obj.creator == request.user or
                request.user.is_superuser):
                return True
            else:
                return False
        else:
            return True


    date_hierarchy = 'edited'
    list_filter = ['stufe__stufe', 'fach__fach', 'reihe__reihe', 'lastEditor']
    save_on_top = True

class MCFrageAdmin (UserAccessInfo):
    fieldsets = [
    ('Die Frage', {'fields': ['frage', 'richtigeAntwort', 'fach', 'stufe', 'reihe', 'schlagworte']}),
    ('Falsche Antworten', {'fields': ['falscheantwort1', 'falscheantwort2', 'falscheantwort3', 'falscheantwort4', 'falscheantwort5', ]}),
    
        ]
    formfield_overrides = {
        models.ManyToManyField: {'widget': Select2MultipleWidget}
    }

    search_fields = ['frage', 'richtigeAntwort',
                     'falscheantwort1',
                     'falscheantwort2',
                     'falscheantwort3',
                     'falscheantwort4',
                     'falscheantwort5',
                     'schlagworte__schlagwort']


class StandardFrageAdmin (UserAccessInfo):
    formfield_overrides = {
        models.ManyToManyField: {'widget': Select2MultipleWidget}
    }

    search_fields = ['frage', 'antwort', 'schlagworte__schlagwort']
    pass


admin.site.register(MCFrage, MCFrageAdmin)
admin.site.register(StandardFrage, StandardFrageAdmin)
