# -*- coding: utf-8 -*-
from django import forms
import models
from django_select2.fields import Select2MultipleChoiceField, Select2ChoiceField
from django_select2.widgets import Select2MultipleWidget, Select2Widget

# basic python infrastrtucture
from pprint import pprint as pp 

class stufeForm (forms.Form):
    # Stufe = forms.fields.ChoiceField (choices=sorted([(x.stufe, x.__unicode__())
    #                                                   for x in models.Stufe.objects.all() ]),
    #                                   required=True)
    Stufe = Select2ChoiceField (choices=sorted([(x.stufe, x.__unicode__())
                                                      for x in models.Stufe.objects.all() ]),
                                widget=Select2Widget(select2_options={'minimumResultsForSearch': 2,
                                                                      'width': u'resolve',
                                                                      'allowClear': 'true',
                                                                      }),
                                      required=True)


class schlagworteForm (forms.Form):

    # Schlagworte = forms.fields.MultipleChoiceField ( )
    Schlagworte = Select2MultipleChoiceField (widget=Select2MultipleWidget(select2_options={'minimumResultsForSearch': 2,
                                                                                            'width': u'resolve',
                                                                                            'allowClear': 'true',
                                                                                            }) )




class KlausurlisteForm (forms.Form):
    mcfragenliste = forms.MultipleChoiceField (label="Welche Multiple-Choice Fragen in die Klausur aufnehmen?",
                                             choices = [],
                                             widget = forms.widgets.CheckboxSelectMultiple())


class Klausurparameter (forms.Form):
    anzahlSchueler = forms.CharField (label="Wieviele Schüler?")
    anzahlVarianten = forms.CharField (label="Wieviele Varianten der Klausur?")
    klausurDatum = forms.DateField (label="An welchem Tag findet die Klausur statt?")
    klausurFach = forms.CharField(label="In welchem Fach?")
    klausurLaufendeNummer =forms.CharField (label="Laufende Nummer der Klausur? (z.B. 7. Test, 9a)")
    klausurBoxtext = forms.CharField(label="WelcherText soll in die Box gesetzt werden?",
                                     widget=forms.Textarea,
                                     initial="Kreuze die korrekte Lösung an. Es gibt für jede Frage nur eine korrekte Lösung.")

class testForm (forms.Form):
    """
    This is only for testing
    """

    testField = forms.fields.MultipleChoiceField()
