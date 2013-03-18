# -*- coding: utf-8 -*-


from django.db import models

# Create your models here.

class Schlagwort(models.Model):
    schlagwort = models.CharField(max_length=200)

    class Meta:
        ordering = ['schlagwort']
	verbose_name_plural = "Schlagworte"

    def __unicode__ (self):
        return self.schlagwort 

class Stufe (models.Model):
    stufe = models.CharField("Klassenstufe und Fach",
			     max_length=10)

    class Meta:
        ordering = ['stufe']
	verbose_name_plural = "Stufen"

    def __unicode__ (self):
        return self.stufe  



class StandardFrage (models.Model):
    frage = models.TextField()
    schlagworte = models.ManyToManyField (Schlagwort,
                                          blank=True)
    stufe = models.ManyToManyField (Stufe,
                                    blank=True)
    antwort = models.TextField()

    platz = models.FloatField(verbose_name="Platz (in cm)",
                              default = 3.0)

    def __unicode__(self):
        return "Q: %s ; A: %s" % (self.frage[:50], self.antwort[:50])


    class Meta:
        verbose_name = "Standard-Frage"
        verbose_name_plural = "Standard-Fragen"
        ordering = ['frage']

class MCFrage(models.Model):
    frage = models.TextField()
    schlagworte = models.ManyToManyField (Schlagwort,
                                          blank=True)
    stufe = models.ManyToManyField (Stufe,
                                          blank=True)
    richtigeAntwort = models.TextField()
    falscheantwort1 = models.TextField(blank=True)
    falscheantwort2 = models.TextField(blank=True)
    falscheantwort3 = models.TextField(blank=True)
    falscheantwort4 = models.TextField(blank=True)
    falscheantwort5 = models.TextField(blank=True)

    def __unicode__(self):
        return "Q: %s ; A: %s" % (self.frage[:50], self.richtigeAntwort[:50])


    class Meta:
	verbose_name_plural = "Multiple-Choice-Fragen"
	verbose_name = "Multiple-Choice-Frage"
        ordering = ['frage']

    def __unicode__ (self):
        return self.frage 
    
    
    
