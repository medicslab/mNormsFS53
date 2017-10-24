#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line version of
Normative morphometric data calculator for FreeSurfer 5.3 (mNormsFS53) - Version 1.0 [for Python version 3]

mNormsFS53 is a free tool to compute normative morphometric values for FreeSurfer 5.3 developed by 
the MEDICS laboratory at the CERVO Research Center / Universite Laval, Quebec, Canada. The normative 
values are produced according to age, sex, estimated intracranial volume (eTIV), scanner manufacturer, 
and scanner magnetic field strength. 

Please cite and refer to the following publications for details:

Potvin et al. (2017). Normative morphometric data for cerebral cortical areas over the lifetime 
of the adult human brain. NeuroImage, 156, 315-339.

Potvin et al. (2017). FreeSurfer cortical normative data for adults using Desikan-Killiany-Tourville 
and Ex vivo protocols. NeuroImage, 156, 43-64.

Potvin et al. (2016). Normative data for subcortical regional volumes over the lifetime of the 
adult human brain. NeuroImage, 137, 9-20.

version 1.0 (september 2017)
----------------------------
initial version

@author: Medics laboratory
Olivier Potvin, Louis Dieumegarde, Simon Duchesne
Centre de Recherche CERVO
Quebec, Canada
"""
import argparse
import sys, os
import csv
from xml.dom import minidom
import bin.NormativeCalculator as NormativeCalculator
#---------------------------
class mylist(list):
    def __contains__(self, other):
        return super(mylist,self).__contains__(other.lower())
#---------------------------
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
#---------------------------
py3 = sys.version_info[0] >= 3
    
lexml = minidom.parse(resource_path(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin/medics.xml'))) ##all the texts in that file
letitle = lexml.getElementsByTagName("title")[0].childNodes[0].nodeValue.strip()
lename = lexml.getElementsByTagName("name")[0].childNodes[0].nodeValue.strip()
ledisclaimer = lexml.getElementsByTagName("disclaimer")[0].childNodes[0].nodeValue.strip()
lesubjects_dir = lexml.getElementsByTagName("subjects_dir")[0].childNodes[0].nodeValue.strip()
leinput_csv = lexml.getElementsByTagName("input_csv")[0].childNodes[0].nodeValue.strip()
leoutput_csv = lexml.getElementsByTagName("output_csv")[0].childNodes[0].nodeValue.strip()
levolumes = lexml.getElementsByTagName("volumes")[0].childNodes[0].nodeValue.strip()
leatlas = lexml.getElementsByTagName("atlas")[0].childNodes[0].nodeValue.strip()

parser = argparse.ArgumentParser(prog=lename, 
                                 usage='%(prog)s [-h] -s <SUBJECTS_DIR> -i <INPUT_CSV> -a <DK|DKT> [-o <OUTPUT_CSV>]',
                                 description=letitle, 
                                 epilog=ledisclaimer, 
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
#required
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument("-s", dest='subjects_dir', help=lesubjects_dir, action='store', required=True) #"--subjects_dir", 
requiredNamed.add_argument("-i", dest='input_csv', help=leinput_csv, action='store', required=True) #"--input", 
leschoix=mylist(['dk','dkt'])
requiredNamed.add_argument("-a", dest='atlas', choices=leschoix, help=leatlas, action='store', required=True) #"--atlas", 
#optional
parser.add_argument("-o", dest='output_csv', help=leoutput_csv, action='store') #"--output", , required=True
parser.add_argument("-v", dest='volumes', action="store_true", help=argparse.SUPPRESS)

if os.name == "nt":
    ## windows not support (as freesurfer is not)
    print
    print(lexml.getElementsByTagName("windows")[0].childNodes[0].nodeValue.strip())
    print
    parser.print_help()
    sys.exit()

#if no arguments at all, show help instead of error message of argparse, and exit
if not len(sys.argv) > 1:
    parser.print_help()
    sys.exit()

args = parser.parse_args()

if args.subjects_dir is not None and args.input_csv is not None and args.atlas is not None:
    #calcul
    leresult = NormativeCalculator.getScoreZ(args, lexml)
    print("")
    print(lexml.getElementsByTagName("leresult")[0].childNodes[0].nodeValue.strip() + " " + os.path.realpath(leresult))
    print("")
else:
    parser.print_help()
    sys.exit()
