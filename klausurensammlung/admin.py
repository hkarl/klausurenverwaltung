from klausurensammlung.models import Schlagwort, Stufe, MCFrage 
from django.contrib import admin

admin.site.register(Schlagwort)
admin.site.register(Stufe)

class MCFrageAdmin (admin.ModelAdmin):
    fieldsets = [
    ('Die Frage', {'fields': ['frage', 'richtigeAntwort', 'stufe', 'schlagworte']}),
    ('Falsche Antworten', {'fields': ['falscheantwort1', 'falscheantwort2', 'falscheantwort3', 'falscheantwort4', 'falscheantwort5', ]}),
    
        ]


admin.site.register(MCFrage, MCFrageAdmin)
