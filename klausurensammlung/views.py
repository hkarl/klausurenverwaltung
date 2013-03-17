# -*- coding: utf-8 -*-

#local files:
import re
import models 
import forms

# django specific: 
import django_tables2
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.conf import settings


# basic python infrastrtucture
from pprint import pprint as pp 
import codecs, os, subprocess 



class stufe(FormView):
    form_class = forms.stufeForm
    template_name = "klausurensammlung/stufe.html"
    success_url = "/klausurensammlung/schlagworte/stufe="
        
    def get_success_url (self):
        target = stufe.success_url + "stufe=" + self.stufe + "/"
        target = stufe.success_url + self.stufe + "/"
        print "target in stufe: ", target
        return target

    def form_valid (self, form):
        print "stufe is valid"
        self.stufe  = form.cleaned_data['Stufe']
        return super(stufe, self).form_valid(form)
        

class schlagworte (View):
    """
    Present the schlageworte multiple choice using a standard view, not the complex mixin FormView
    """

    def get (self, request, stufe):
        print "in get", stufe

        ff = forms.schlagworteForm ()
        # ff.fields['Schlagworte'].choices = (('a','a'),
        #                                     ('b','b'),
        #                                     ('c','c'),
        #                                     ('d','d'),)
        ff.fields['Schlagworte'].choices = ( (x['schlagworte'],
                                              models.Schlagwort.objects.get (pk=x['schlagworte']).__unicode__())
                                              for x in
                                              models.MCFrage.objects.all().filter (stufe__stufe__exact = stufe).values('schlagworte').distinct())

        pp (ff.fields['Schlagworte'].choices)

        return render (request,
                       'klausurensammlung/schlagworte.html',
                        {'form': ff})


    def post (self, request, stufe):
        # print 'in post', stufe
        # print request.POST
        ids = request.POST.getlist('Schlagworte')
        # print ids

        schlagwortIDs = [int(x) for x in ids]
        # print schlagwortIDs

        # berechne die Fragen-IDs
        # print "fragen"
        fragenIDs = []

        for x in models.MCFrage.objects.all():
            thisQuestionSchlagwortIDs = [y.pk for y in x.schlagworte.all()]
            # print x.pk, thisQuestionSchlagwortIDs
            # print set(schlagwortIDs).intersection(set(thisQuestionSchlagwortIDs))
            if bool(set(schlagwortIDs).intersection(set(thisQuestionSchlagwortIDs))):
                fragenIDs.append(str(x.pk))


        pp(fragenIDs)

        # return redirect ('klausur', stufe = stufe, ids = ','.join(ids))
        # return redirect ('/klausurensammlung/klausur/%s/' %
        #                 (stufe))
        return redirect ('/klausurensammlung/klausur/stufe=%s/sw=%s/fragen=%s/' %
                         (stufe,
                          ','.join([str(x) for x in schlagwortIDs]),
                          ','.join(fragenIDs)))



    
class klausur(View):
    def get (self, request, stufe, swIds, ids):

        # pp(request)

        ## pp (request.GET)

        print "in klausur get"
        print ids.split(',')
        print swIds


        # filtere alle Fragen nach der verlangten Stufe
        # fragen = models.MCFrage.objects.all()
        fragen = models.MCFrage.objects.filter(stufe__stufe__exact = stufe)


        idlist = ids.split(',')

        fragenstrings = [(x.pk, "'%s'" % x.__unicode__())
                         for x in
                         fragen.filter(id__in=idlist)]

        pp (fragenstrings)


        ff = forms.KlausurlisteForm()
        ff.fields['fragenliste'].choices = fragenstrings

        return render (request,
                'klausurensammlung/klausurListe.html',
                {'form': ff,
                 'stufe': stufe,
                 'schlagworte': ', '.join([x.__unicode__()
                                 for x in models.Schlagwort.objects.filter(id__in =
                                    swIds.split(','))]),
                 }
                )

    def post (self, request, stufe, swIds, ids):
        # print "klausr in post"
        # print "ids", ids
        # selectedIds = [x for x in request.POST.getlist ('fragenliste')]
        # print "selected IDs", selectedIds

        return redirect ('/klausurensammlung/makePDF/%s/' % ','.join(request.POST.getlist ('fragenliste')))


class makePDF(View):

    def get(self, request, ids):
        # print request.GET

        ff = forms.Klausurparameter

        return render (request,
                       'klausurensammlung/parameter.html',
                        {'fragenliste': ids,
                         'form': ff})

    def post (self, request, ids):

        print "makePDF post"

        ff = forms.Klausurparameter(request.POST)

        if not ff.is_valid():
            print "form not valid"
            return render (request,
                           'klausurensammlung/parameter.html',
                           {'fragenliste': ids,
                            'form': ff})


        # Felder des Formats auswerten:
        anzahlSchueler = ff.cleaned_data['anzahlSchueler']
        anzahlVarianten = ff.cleaned_data['anzahlVarianten']
        klausurDatum = ff.cleaned_data['klausurDatum']
        klausurFach = ff.cleaned_data['klausurFach']
        klausurLaufendeNummer = ff.cleaned_data['klausurLaufendeNummer']
        klausurBoxtext = ff.cleaned_data['klausurBoxtext']

        # die richtien Fragen aus der DAtenbank holen:
        fragen = models.MCFrage.objects.filter (id__in = ids.split(','))

        pp ([x.frage for x in fragen])
        # write questions.tex

        questionsList = []
        for x in fragen:
            falscheAntwort = ""
            # check the wrong ansers
            if x.falscheantwort1:
                falscheAntwort += r"\choice " + x.falscheantwort1 + "\n"
            if x.falscheantwort2:
                falscheAntwort += r"\choice " + x.falscheantwort2 + "\n"
            if x.falscheantwort3:
                falscheAntwort += r"\choice " + x.falscheantwort3 + "\n"
            if x.falscheantwort4:
                falscheAntwort += r"\choice " + x.falscheantwort4 + "\n"
            if x.falscheantwort5:
                falscheAntwort += r"\choice " + x.falscheantwort5 + "\n"


            questionsList.append(r"""
\question %s
\\begin{checkboxes}
\CorrectChoice %s
%s\end{checkboxes}
"""  % ( x.frage, x.richtigeAntwort, falscheAntwort))

        questions = r"""
\\begin{questions}
%s
\end{questions}
""" %  '\n'.join(questionsList)

        # print questions
        # print settings.LATEXDIR
        # print os.getcwd()

        fp = open (os.path.join(settings.LATEXDIR, "questions.tex"), 'w')
        fp.write(questions.encode('utf-8'))
        fp.close()


        # header schreiben
        header = r"""
\\newcommand{\klausurdatum}{%s}
\\newcommand{\klausurfach}{%s}
\\newcommand{\klausurnummer}{%s}
\\newcommand{\\boxtext}{%s}
        """ % (klausurDatum, klausurFach, klausurLaufendeNummer,
                klausurBoxtext)

        fp = open (os.path.join(settings.LATEXDIR, "header.tex"), 'w')
        fp.write (header.encode('utf-8'))
        fp.close


        # flatten the input file
        fp = codecs.open (os.path.join (settings.LATEXDIR, "klausur-template.tex"), 'r', encoding='utf-8')
        klausur = fp.read()
        fp.close()

        # replace header and questions
        klausur = re.sub(r'\\input{header}', header, klausur)
        klausur = re.sub(r'\\input{questions}', questions, klausur)
        fp = open (os.path.join(settings.LATEXDIR, "klausur.tex"), 'w')
        fp.write (klausur.encode('utf-8'))
        fp.close()


        # run permuter on it
        permuterOut = open (os.path.join(settings.LATEXDIR, 'permuter.out'), 'w')
        permuterErr = open (os.path.join(settings.LATEXDIR, 'permuter.err'), 'w')
        print os.getcwd()
        print os.path.join(settings.BINDIR, settings.PERMUTER)
        print settings.LATEXDIR
        permuterProcess  = subprocess.Popen ([os.path.join(os.getcwd(),
                                                   settings.BINDIR,
                                                   settings.PERMUTER),
                                     "-n", anzahlVarianten,
                                     "-p",
                                     "-l",
                                     "-i", "klausur.tex",
                                     ],
                                     cwd = settings.LATEXDIR,
                                     stderr=permuterErr,
                                     stdout = permuterOut)

        permuterProcess.wait()
        permuterOut.close()
        permuterErr.close()

        permuterRetcode = permuterProcess.returncode

        # generate the PDF file
        inputNurLoesungen = ["klausur-%d-loesung.pdf" % (x+1) for x in range(int(anzahlVarianten))]
        inputNurAufgaben = []
        for i in range(int(anzahlSchueler)):
            v = (i % int(anzahlVarianten)) + 1
            # print v
            inputNurAufgaben.append("klausur-%d.pdf" % v)

        inputAlles = inputNurLoesungen + inputNurAufgaben

        # print inputNurLoesungen
        # print inputNurAufgaben
        # print inputAlles

        concatReval = {}
        concatReval['loesung'] = self.concatPDFs(inputNurLoesungen, "loesungen")
        concatReval['aufgaben'] = self.concatPDFs(inputNurAufgaben, "aufgaben")
        concatReval['komplett'] = self.concatPDFs(inputAlles, "komplett")



    # return the pdf file

        
        return render (request,
                       "klausurensammlung/fertig.html",
                        {'texVarianten': ["klausur-%d.tex" % (x+1)
                                           for x in range(int(anzahlVarianten))],
                         'klausurVarianten': ["klausur-%d.pdf" % (x+1)
                                          for x in range(int(anzahlVarianten))],
                         'loesungVarianten': ["klausur-%d-loesung.pdf" % (x+1)
                                          for x in range(int(anzahlVarianten))],
                         'permuterRetcode': permuterRetcode,
                         })
    

    def concatPDFs (self, l, s):
        concatOut = open (os.path.join(settings.LATEXDIR, 'concat-%s.out' % s), 'w')
        concatErr = open (os.path.join(settings.LATEXDIR, 'concat-%s.err' % s), 'w')

        concatProcess  = subprocess.Popen ([settings.PDFTK] + l + ['output', s + '.pdf'],
                                             cwd = settings.LATEXDIR,
                                             stderr=concatErr,
                                             stdout = concatOut)

        concatProcess.wait()
        concatOut.close()
        concatErr.close()

        return concatProcess.returncode

class testView (FormView):

    template_name = "klausurensammlung/test.html"
    form_class = forms.testForm
    success_url = "success.html"

    choices=(('a','a'),
             ('b','b'),
             ('c','c'),
             ('d','d'),)

    def get_initial(self):
        print "initial", self.request.path, self.request.GET

        initial = {}
        initial['testField'] = 'a'
        return initial


    def form_valid(self, f):
        print "form is valid"
        print "selected: ", f.cleaned_data

        return super(testView, self).form_valid(f)


