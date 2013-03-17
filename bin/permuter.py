#!/usr/bin/python 
# permutation script for LaTeX exams

import sys
import argparse
import re
import pprint 
import random
import string
import subprocess
# import Pashua
import os


mcstrings = ['choices', 'oneparchoices', 'checkboxes', 'oneparcheckboxes']

def shuffle_mc (x):

    for t in mcstrings:
        
        beginstrings = r'\\begin{' + t + '}'
        endstrings = r'\\end{' + t + '}' 
        try:
            pre, body = re.split (beginstrings, x)
            body, post = re.split ( endstrings, body)
            #print t, '---------', pre, '---------',  body # , '----------', post

            body = re.sub (r'\\CorrectChoice', r'\\choice CORRECTCHOICE', body)

            ## print "1:"
            ## pprint.pprint (body)

            body = re.split (r'\\choice', body)
            body = [str.strip(t3) for t3 in body if (not str.isspace(t3))]
            # print [str.isspace(t3) for t3 in body]

            ## print "2:"
            ## pprint.pprint (body)

            random.shuffle(body)
            ## print "3:"
            ## pprint.pprint (body)


            return (pre +
                    r'\begin{' + t + '}\n' +
                    '\n'.join([re.sub(r'\\choice CORRECTCHOICE', r'\\CorrectChoice', (r'\choice ' + t2))
                               for t2 in body]) + '\n' +
                    r'\end{' + t +  '}' ) 
        except:
            continue 

    return x 

def main():
    parser = argparse.ArgumentParser(description='Randomize exam questins.', epilog="Good luck!")
    parser.add_argument ('-i', '--infile', dest = 'infile', help='Input file, latex file based on the exam class',
                         default = 'klausur.tex', required =True)
    parser.add_argument ('-n', '--number', dest = 'n', help='Number of variants to produce', default = 1, type= int )
    parser.add_argument ('-p', '--pdf', dest = 'pdf', help='Produce PDF files?',
                         default = False, action='store_true')
    parser.add_argument ('-q', '--questions', dest = 'questions', help='If present, main questions are NOT randomized; default= they are!', action='store_false',
                         default = True )
    parser.add_argument ('-m', '--multiplechoice', dest = 'mc',
                         help='If present, multiple choice questions are NOT randomized; default= they are!',
                         action='store_false',
                         default = True )
    parser.add_argument ('-s', '--schueler', dest = 'schueler',
                         help='If present, PRINT out a corresponding number of copies',
                         default = 0, type=int)
    parser.add_argument ('-l', '--loesung', dest = 'loesung',
                         help='If present, generate the solution.',
                         default=False, action='store_true') 
    parser.add_argument ('-L', '--Loesung', dest = 'printloesung',
                         help='If present, generate AND PRINT the solution.',
                         default=False, action='store_true') 
    parser.add_argument ('-g', '--gui', dest = 'gui', help='Ignore all options except -i and start a GUI dialog',
                         default = False, action='store_true')
    

    args = parser.parse_args ()

    # should we start a gui to fill in the parameters?
    if args.gui:
        PashuaConf = """
        #
# Titel: 
*.title = Klausurenverwuerfeler

# Datei: 
infile.type = openbrowser
infile.label = Welche tex-Datei? 
infile.default = %s
infile.tooltip = Welche tex-Datei soll verwuerfelt werden? Format des exam-Packages einhalten!


# Wieviele Varianten?
n.type = textfield
n.label = Wieviele Varianten der Klausur sollen produziert werden?
n.default = 2
n.tooltip = Es werden entsprechende viele tex bzw. pdf-Dateien erzeugt; jede Datei enthaelt eine Variante der Klausur.

pdf.type = checkbox
pdf.label = PDFs erzeugen?
pdf.tooltip = Sollen fuer die erzeugten Varianten die PDF-Dateien direkt erzeugt werden?
pdf.default = 1

questions.type = checkbox
questions.label = Fragen verwuerfeln?
questions.tooltip = Sollen die Fragen in unterschiedlicher Reihenfolge in der Klausur auftauchen?
questions.default = 1

mc.type = checkbox
mc.label = MC-Optionen verwuerfeln?
mc.tooltip = Sollen (innerhalb einer Frage) die multiple-choice-Antwortoptionen verwuerfelt werden?
mc.default = 1

loesung.type = checkbox
loesung.label = Loesung erzeugen?
loesung.tooltip = Fuer jede Variante wird eine PDF-Datei mit der Loesung erzeugt
loesung.default = 1 

printloesung.type = checkbox 
printloesung.label = Loesung ausdrucken?
printloesung.tooltip = Fuer jede Variante wird ein Exemplar der Loesung ausgedruckt
printloesung.default = 0 

# Wieviel Schueler?
schueler.type=textfield
schueler.label=Wieviele Exemplare ausdrucken? 
schueler.default=0
schueler.tooltip=Nur relevant, wenn auch ausgedruckt werden soll! 

cb.type=cancelbutton
""" % args.infile
        # print PashuaConf 
        Result = Pashua.run(PashuaConf)
        for Key in Result.keys():
            print "%s = %s" % (Key, Result[Key])
            print "Type: ", type(Result[Key])

        if Result['cb'] == '1':
            print "exiting"
            return 0  

        args.infile = Result['infile']
        args.n = int(Result['n'])
        args.pdf = Result['pdf'] == '1'
        args.questions = Result['questions'] == '1'
        args.mc = Result['mc'] == '1'
        args.loesung = Result['loesung'] == '1'
        args.printloesung = Result['printloesung'] == '1'
        args.schueler = int(Result['schueler'])

    print args


    # check which options imply which other ones:
    if args.printloesung:
        args.loesung = True
    if args.schueler > 0:
        args.pdf = True 

    # get rid of a possible '.tex' at infile
    args.infile = re.sub(r'\.tex$', '', args.infile)

    args.inpath = os.path.dirname (args.infile)
    if args.inpath == "":
        args.inpath = "./" 
    print "inpath: " + args.inpath 
    
    # read in infile: 

    try:
        f = open (args.infile  + '.tex', 'r')
    except:
        print "Could not open infile - please check filename!"
        return 

    intext = f.read()
    f.close()
    # print intext
    groups = re.split (r'\\question', intext)

    prolog = groups[0]
    groups = groups[1:]
    lastquestion, epilog = re.split (r'\\end{questions}', groups[-1])
    groups[-1] = lastquestion

    ## print "1: ------------"

    ## print prolog
    ## print "2: ------------"
    ## pprint.pprint (groups )
    ## print "3: ------------"
    ## print epilog
    
    # chop it into prolog, questions, epilog
    # randomize questions, if desired
    for i in range(1, args.n+1):
        # print i
        outtext = ''
        
        if args.questions:
            random.shuffle (groups)

        if args.mc:
            groups = [shuffle_mc(x) for x in groups]

        # outtext = (prolog + '\n'.join([r'\question' + x for x in groups]) + r'\end{questions}' + epilog)
        outtext = (prolog +   '\\pagebreak[1] \n'.join([r'\begin{samepage}' + r'\question' + x +
                                         r'\end{samepage}'
                                         for x in groups]) +
            r'\end{questions}' + epilog) 
        # print outtext

        try:
            f = open (args.infile + '-' + str(i) + '.tex', 'w')
        except:
            print "Could not open output file  - please check filename: " + args.infile + '-' + str(i) + '.tex'
            return

        f.write(outtext)
        f.close()
        


    #produce the pdfs?
    if args.pdf:
        os.chdir (args.inpath)
        for i in range(1, args.n+1):

            aufgabe = args.infile + '-' + str(i)

            # loesung erzeugen?
            if args.loesung:
                subprocess.call (["pdflatex",  "-interaction=nonstopmode", r"\def\loesung{}\input{"+ aufgabe + "}"])
                subprocess.call (["pdflatex",  "-interaction=nonstopmode", r"\def\loesung{}\input{"+ aufgabe + "}"])
                subprocess.call (["pdflatex",  "-interaction=nonstopmode", r"\def\loesung{}\input{"+ aufgabe + "}"])
                subprocess.call (["mv", aufgabe+".pdf", aufgabe+"-loesung.pdf"])


            subprocess.call (["pdflatex",  "-interaction=nonstopmode", aufgabe])
            subprocess.call (["pdflatex",  "-interaction=nonstopmode", aufgabe])
            subprocess.call (["pdflatex",  "-interaction=nonstopmode", aufgabe])
            

            # loesung ausdrucken? 
            if args.printloesung:
                subprocess.call (["lpr", "-o",  "sides=two-sided-long-edge",
                                  aufgabe+"-loesung.pdf"])



    # print the questions directly?
    if args.schueler > 0:
        print args.schueler
        for s in range(1,args.schueler+1):
            variant = (s % args.n) + 1
            # print s, variant
            subprocess.call (["lpr",  "-o",  "sides=two-sided-long-edge",
                              args.infile + '-' + str(variant) + '.pdf'])



    if args.gui:
        pashuaConf = """
*.title = Klausur verwuerfelt!
*.autocloseinterval = 15
tx.type = text 
tx.text= Klausur wurde vollstaendig verwuerfelt!
"""
        res = Pashua.run (pashuaConf)
        
if __name__ == "__main__":
    main()
    
    
    
