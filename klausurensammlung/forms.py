# -*- coding: utf-8 -*-
from django import forms
import models


# basic python infrastrtucture
from pprint import pprint as pp 

class stufeForm (forms.Form):
    Stufe = forms.fields.ChoiceField (choices=sorted([(x.stufe, x.__unicode__())
                                                      for x in models.Stufe.objects.all() ]),
                                                      required=True)


class schlagworteForm (forms.Form):

    Schlagworte = forms.fields.MultipleChoiceField (
        ## choices =
        ##                                     [(x.id, x.__unicode__())
        ##                                      for x in models.Schlagwort.objects.all()],
                                            widget=forms.CheckboxSelectMultiple)


    # def is_valid(self):
    #     print "SchlagworteForm is_valid"
    #     print self.data['Schlagworte']
    #     pp (self.is_bound)
    #     pp (self.errors)
    #     pp (self._errors)
    #     res = super (schlagworteForm, self).is_valid()
    #     print "res in is_valid:", res
    #     pp (self.is_bound)
    #     pp (self.errors)
    #     pp (self._errors)
    #     if res:
    #         print "further checking"
    #         print self.cleaned_data
    #
    #     return res
        

    ## def narrowSchlagworte(self):
    ##     print "narrowSchlagworte:"
    ##     pp(self.cleaned_data) 
    ##     if ((not (self.cleaned_data['Stufe'] == '-1' or
    ##               self.cleaned_data['Stufe'] == ''
    ##              )) and
    ##         (self.cleaned_data['Schlagworte'] ==  [])):
    ##         print "reselect schlagworte"
    ##         # find all Schlagworte that appear in Klausuren that have the corresponding class
    ##         qsKlausuren = models.MCFrage.objects.all().filter (stufe__stufe__exact =
    ##                                              self.cleaned_data['Stufe'])

    ##         schlagw = qsKlausuren.values('schlagworte').distinct()
    ##         pp (qsKlausuren.all())
    ##         pp (schlagw.all())
            
            
    ##         self.fields['Schlagworte'].choices = [ (x['schlagworte'],
    ##                                                 models.Schlagwort.objects.get (pk=x['schlagworte']).schlagwort)
    ##                                                 for x in schlagw.all()]
    ##     print "----"


class KlausurlisteForm (forms.Form):
    fragenliste = forms.MultipleChoiceField (label="Welche Fragen in die Klausur aufnehmen?",
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
