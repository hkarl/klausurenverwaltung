from klausurensammlung.models import Schlagwort, Stufe, MCFrage, StandardFrage
from django.contrib import admin
from django.db import models
from django_select2.widgets import Select2MultipleWidget

admin.site.register(Schlagwort)
admin.site.register(Stufe)

class MCFrageAdmin (admin.ModelAdmin):
    fieldsets = [
    ('Die Frage', {'fields': ['frage', 'richtigeAntwort', 'stufe', 'schlagworte']}),
    ('Falsche Antworten', {'fields': ['falscheantwort1', 'falscheantwort2', 'falscheantwort3', 'falscheantwort4', 'falscheantwort5', ]}),
    
        ]
    formfield_overrides = {
        models.ManyToManyField: {'widget': Select2MultipleWidget}
    }
    list_filter = ['stufe__stufe']
    search_fields = ['frage', 'richtigeAntwort',
                     'falscheantwort1',
                     'falscheantwort2',
                     'falscheantwort3',
                     'falscheantwort4',
                     'falscheantwort5',
                     'schlagworte__schlagwort']


class StandardFrageAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': Select2MultipleWidget}
    }
    list_filter = ['stufe__stufe']
    search_fields = ['frage', 'antwort', 'schlagworte__schlagwort']
    pass


admin.site.register(MCFrage, MCFrageAdmin)
admin.site.register(StandardFrage, StandardFrageAdmin)
