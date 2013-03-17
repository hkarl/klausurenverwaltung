# -*- coding: utf-8 -*-


from django.db import models

# Create your models here.

class Schlagwort(models.Model):
    schlagwort = models.CharField(max_length=200)

    class Meta:
	verbose_name_plural = "Schlagworte"

    def __unicode__ (self):
        return self.schlagwort 

class Stufe (models.Model):
    stufe = models.CharField("Klassenstufe und Fach",
			     max_length=10)

    class Meta:
	verbose_name_plural = "Stufen"

    def __unicode__ (self):
        return self.stufe  



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

    class Meta:
	verbose_name_plural = "Multiple-Choice-Fragen"
	verbose_name = "Multiple-Choice-Frage" 

    def __unicode__ (self):
        return self.frage 
    
    
    
