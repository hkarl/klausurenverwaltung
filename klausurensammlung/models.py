# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse 
from django.http import HttpResponseRedirect 
from model_utils.managers import InheritanceManager


# Create your models here.

# basic user and access management for the questions
# abstract base classe:


class UserAccess (models.Model):
    # note: when the user is deleted, the user field is set to NULL
    creator = models.ForeignKey (User, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name="%(app_label)s_creator_%(class)s_related",
                                 editable=False)
    lastEditor = models.ForeignKey (User, blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name="%(app_label)s_lastEditor_%(class)s_related",
                                    editable=False)

    created = models.DateField(editable=False)
    edited = models.DateField(editable=False)

    class Meta:
        abstract = True



################################
# content models

class Schlagwort(models.Model):
    schlagwort = models.CharField(max_length=200)

    class Meta:
        ordering = ['schlagwort']
        verbose_name_plural = "Schlagworte"

    def __unicode__ (self):
        return self.schlagwort


################################


class Stufe (models.Model):
    stufe = models.CharField("Klassenstufe",
                 max_length=10)

    class Meta:
        ordering = ['stufe']
        verbose_name_plural = "Stufen"

    def __unicode__ (self):
        return self.stufe

################################

class Fach (models.Model):
    fach = models.CharField("Fach",
                            max_length=200)

    class Meta:
        ordering = ['fach']
        verbose_name_plural = "Fächer"

    def __unicode__ (self):
        return self.fach

################################

class Reihe (models.Model):
    reihe = models.CharField("Reihe",
                             max_length=200)

    class Meta:
        ordering = ['reihe']
        verbose_name_plural = "Reihen"

    def __unicode__ (self):
        return self.reihe

    # basic question


################################
# abstract base class:

class basicFrage (UserAccess):
    # note: not abstract, but should not be editable. vMake sure to build inlines for the derived
    # classes in admin

    fach = models.ManyToManyField (Fach,
                                    blank=True)


    stufe = models.ManyToManyField (Stufe,
                                    blank=True)

    reihe = models.ManyToManyField (Reihe,
                                    blank=True)

    schlagworte = models.ManyToManyField (Schlagwort,
                                          blank=True)

    objects = InheritanceManager()



################################

class StandardFrage (basicFrage):
    frage = models.TextField()
    antwort = models.TextField()

    platz = models.FloatField(verbose_name="Platz (in cm)",
                              default = 3.0)

    def __unicode__(self):
        return "Q: %s ; A: %s" % (self.frage[:50], self.antwort[:50])

    def get_absolute_url (self):
        r = reverse ('standardfrage', args=[str(self.id)])
        return r

    class Meta (basicFrage.Meta):
        verbose_name = "Standard-Frage"
        verbose_name_plural = "Standard-Fragen"
        ordering = ['frage']


################################


class MCFrage(basicFrage):
    frage = models.TextField()
    richtigeAntwort = models.TextField()
    falscheantwort1 = models.TextField(blank=True)
    falscheantwort2 = models.TextField(blank=True)
    falscheantwort3 = models.TextField(blank=True)
    falscheantwort4 = models.TextField(blank=True)
    falscheantwort5 = models.TextField(blank=True)

    def __unicode__(self):
        return "Q: %s ; A: %s" % (self.frage[:50], self.richtigeAntwort[:50])

    def get_absolute_url (self):
        r = reverse ('mcfrage', args=[str(self.id)])
        return r

    class Meta (basicFrage.Meta):
        verbose_name_plural = "Multiple-Choice-Fragen"
        verbose_name = "Multiple-Choice-Frage"
        ordering = ['frage']




