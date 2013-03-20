# -*- coding: utf-8 -*-

#local files:
import re
import models 
import forms

# django specific: 
# import django_tables2
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# basic python infrastrtucture
from pprint import pprint as pp 
import codecs, os, subprocess 



class stufe(FormView):
    form_class = forms.stufeForm
    template_name = "klausurensammlung/stufe.html"
    success_url = "/klausurensammlung/schlagworte/stufe="
        
    def get_success_url (self):
        # target = stufe.success_url + "stufe=" + self.stufe + "/"

        target = stufe.success_url + str(self.stufe.stufe) + "/"
        # print "target in stufe: ", target
        return target

    def form_valid (self, form):
        # print "stufe is valid"
        self.stufe  = form.cleaned_data['Stufe']
        return super(stufe, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(stufe, self).dispatch(*args, **kwargs)

class schlagworte (View):
    """
    Present the schlageworte multiple choice using a standard view, not the complex mixin FormView
    """

    @method_decorator (login_required)
    def get (self, request, stufe):
        # print "in get", stufe

        ff = forms.schlagworteForm ()
        # ff.fields['Schlagworte'].choices = (('a','a'),
        #                                     ('b','b'),
        #                                     ('c','c'),
        #                                     ('d','d'),)

        mcSchlagwortIds = [x['schlagworte'] for x in
                           models.MCFrage.objects.all().filter (stufe__stufe__exact = stufe).values('schlagworte').distinct()]
        standardFrageSchlagwortIds = [x['schlagworte'] for x in
                                      models.StandardFrage.objects.all().filter (stufe__stufe__exact = stufe).values('schlagworte').distinct()]

        # pp(mcSchlagwortIds)

        schlagwortIds = set(mcSchlagwortIds) | set (standardFrageSchlagwortIds)
        # pp(schlagwortIds)
        ff.fields['Schlagworte'].choices = ( (x,
                                              models.Schlagwort.objects.get (pk=x).__unicode__())
                                              for x in schlagwortIds
                                              )

        # pp (ff.fields['Schlagworte'].choices)

        return render (request,
                       'klausurensammlung/schlagworte.html',
                        {'form': ff})


    @method_decorator (login_required)
    def post (self, request, stufe):
        # print 'in post', stufe
        # print request.POST
        ids = request.POST.getlist('Schlagworte')
        # print ids

        schlagwortIDs = [int(x) for x in ids]
        # print schlagwortIDs

        # berechne die Fragen-IDs
        # print "fragen"
        mcfragenIDs = []

        for x in models.MCFrage.objects.all():
            thisQuestionSchlagwortIDs = [y.pk for y in x.schlagworte.all()]
            # print x.pk, thisQuestionSchlagwortIDs
            # print set(schlagwortIDs).intersection(set(thisQuestionSchlagwortIDs))
            if bool(set(schlagwortIDs).intersection(set(thisQuestionSchlagwortIDs))):
                mcfragenIDs.append(str(x.pk))

        # pp(mcfragenIDs)

        # fuer die Standardfragen versuchen wir mal eine andere Iteration:
        # print "standardfragen"
        standardFragenIDs = set()
        for s in schlagwortIDs:
            # print models.Schlagwort.objects.get(pk=s)
            qs = models.StandardFrage.objects.filter(schlagworte__id__exact = s)
            # print set([x.id for x in qs])
            standardFragenIDs |= set([x.id for x in qs])

        standardFragenIDs = list(standardFragenIDs)
        # print standardFragenIDs

        # return redirect ('klausur', stufe = stufe, ids = ','.join(ids))
        # return redirect ('/klausurensammlung/klausur/%s/' %
        #                 (stufe))
        return redirect ('/klausurensammlung/klausur/stufe=%s/sw=%s/stfragen=%s/mcfragen=%s/' %
                         (stufe,
                          ','.join([str(x) for x in schlagwortIDs]),
                          ','.join([str(x) for x in standardFragenIDs]),
                          ','.join(mcfragenIDs)))



    
class klausur(View):
    @method_decorator (login_required)
    def get (self, request, stufe, swIds, stids, mcids):

        # pp(request)

        ## pp (request.GET)

        # print "in klausur get"
        # print mcids.split(',')
        # print swIds


        # filtere alle Fragen nach der verlangten Stufe
        # fragen = models.MCFrage.objects.all()
        mcfragen = models.MCFrage.objects.filter(stufe__stufe__exact = stufe)
        stfragen = models.StandardFrage.objects.filter(stufe__stufe__exact = stufe)


        # fill in the form
        ff = forms.KlausurlisteForm()

        # mc fragen:
        if mcids:
            mcidlist = mcids.split(',')
            fragenstrings = [(x.pk, "%s" % x.__unicode__())
                             for x in
                             mcfragen.filter(id__in=mcidlist)]
            ff.fields['mcfragenliste'].choices = fragenstrings

        # standardfragen
        if stids:
            stidlist = stids.split(',')
            ff.fields['stfragenliste'].choices = [(x.pk, x.__unicode__() )
                                                    for x in
                                                    stfragen.filter(id__in=stidlist)]

        return render (request,
                'klausurensammlung/klausurListe.html',
                {'form': ff,
                 'stufe': stufe,
                 'schlagworte': ', '.join([x.__unicode__()
                                 for x in models.Schlagwort.objects.filter(id__in =
                                    swIds.split(','))]),
                 }
                )

    @method_decorator (login_required)
    def post (self, request, stufe, swIds, stids, mcids):
        # print "klausr in post"
        # print "ids", ids
        # selectedIds = [x for x in request.POST.getlist ('fragenliste')]
        # print "selected IDs", selectedIds

        return redirect ('/klausurensammlung/makePDF/st=%s/mc=%s/' %
                         (','.join(request.POST.getlist ('stfragenliste')),
                          ','.join(request.POST.getlist ('mcfragenliste'))))


class makePDF(View):

    @method_decorator (login_required)
    def get(self, request, stids, mcids):
        # print request.GET

        ff = forms.Klausurparameter

        return render (request,
                       'klausurensammlung/parameter.html',
                        {'stfragenliste': stids,
                         'mcfragenliste': mcids,
                         'form': ff})

    @method_decorator (login_required)
    def post (self, request, stids, mcids):

        # print "makePDF post"

        ff = forms.Klausurparameter(request.POST)

        if not ff.is_valid():
            # print "form not valid"
            return render (request,
                           'klausurensammlung/parameter.html',
                           {'stfragenliste': stids,
                            'mcfragenliste': mcids,
                            'form': ff})


        # Felder des Formats auswerten:
        anzahlSchueler = ff.cleaned_data['anzahlSchueler']
        anzahlVarianten = ff.cleaned_data['anzahlVarianten']
        klausurDatum = ff.cleaned_data['klausurDatum']
        klausurFach = ff.cleaned_data['klausurFach']
        klausurLaufendeNummer = ff.cleaned_data['klausurLaufendeNummer']
        klausurBoxtext = ff.cleaned_data['klausurBoxtext']


        # pp ([x.frage for x in mcfragen])
        questionsList = []
        # write questions.tex

        # hier die MC-Fragen
        # die richtien Fragen aus der DAtenbank holen:
        if mcids:
            mcfragen = models.MCFrage.objects.filter (id__in = mcids.split(','))
            for x in mcfragen:
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


        # und hier die STandardfragen
        if stids:
            stfragen = models.StandardFrage.objects.filter (id__in = stids.split(','))
            for x in stfragen:
                print type(x.antwort)
                questionsList.append(ur"""
\question {0:s}
\\begin{{solutionorlines}}[{1:s}cm]
{2:s}
\\end{{solutionorlines}}
""".format(x.frage, str(x.platz), x.antwort))


        questions = ur"""
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
        """ % (klausurDatum.strftime('%d.%m.%Y'), klausurFach, klausurLaufendeNummer,
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
        # print os.getcwd()
        # print os.path.join(settings.BINDIR, settings.PERMUTER)
        # print settings.LATEXDIR
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



