#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
from math import log #use in eval(string)
import csv
import time
from bin import medics

# Tables to read
tables = [["lh.aparc.DKTatlas40.stats","lh.BA.stats","lh.entorhinal_exvivo.stats","rh.aparc.DKTatlas40.stats","rh.BA.stats","rh.entorhinal_exvivo.stats","aseg.stats"],
          ["lh.aparc.stats","lh.BA.stats","lh.entorhinal_exvivo.stats","rh.aparc.stats","rh.BA.stats","rh.entorhinal_exvivo.stats","aseg.stats"]]
normes = [["DKT"],["DK"]]
##########################################################################################
##########################################################################################
def file_save(ledata, csvpath, args, efface):
    if efface:
        os.unlink(csvpath)
    with open(csvpath, 'a') as ff:
        for i, val in enumerate(ledata):
            w = csv.writer(ff, dialect='excel')
            w.writerow(val)
    
##########################################################################################
def affiche_erreur(lexml, letag, lextra = ""):
    print("Error :")
    print(lexml.getElementsByTagName(letag)[0].childNodes[0].nodeValue.strip() + lextra)
    print("")
    print("Use '" + lexml.getElementsByTagName("name")[0].childNodes[0].nodeValue.strip() + " -h' for help.")
    print("")
    sys.exit()

##########################################################################################
def affiche_warning(lexml, letag, lextra = ""):
    print("")
    print(lexml.getElementsByTagName(letag)[0].childNodes[0].nodeValue.strip() + lextra)
    print("")

##########################################################################################
def parse_aparc(lexml, lefolder, patient_name, tableFile, ledata):

    filepath = os.path.join(lefolder, patient_name, "stats", tableFile)

    if os.path.isfile(filepath) is False:
        return ledata
    # find patient's line
    for p, val in enumerate(ledata):
        for q, lav in enumerate(val):
            if lav == patient_name:
                index_patient = p

    # add data from stats files
    datatemp = medics.createTuple(filepath)
    lesmesures = "SVT"
    for i, val in enumerate(datatemp):
        ### MEASURE LINES
        if val[0].find("Measure") >= 0 and tableFile.find("aparc") >= 0 and val[1] != "NumVert":
            #need to transform the names for uniformity
            if re.search(r'^(.*)(WhiteSurfArea)(.*)$', val[1]):
                datatemp[i][1] = "Cortex" + "_" + tableFile[:1].upper() + "S"
            if re.search(r'^(.*)(MeanThickness)(.*)$', val[1]):
                datatemp[i][1] = "Cortex" + "_" + tableFile[:1].upper() + "T"
            if datatemp[i][1] in ledata[0]:
                # verify if encounter same structure with different value
                for j, val1 in enumerate(ledata[0]):
                    if ledata[0][j] == datatemp[i][1]:
                        if ledata[index_patient][j] != datatemp[i][3] and ledata[index_patient][j] != '':
                            affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                        ledata[index_patient][j] = datatemp[i][3]
            else:
                # Adding column to array
                ledata = [x + [''] for x in ledata]
                ledata[0][len(ledata[0])-1] = datatemp[i][1] #+ "_" + tableFile[:1].upper() #tableFile[:1] + "_" + datatemp[i][1]
                ledata[index_patient][len(ledata[0])-1] = datatemp[i][3]
        ### STRUCTURES WITHOUT #
        if val[0][:1] != '#' and len(val[0]) > 4:
            if re.search(r'^(.*)(h.entorhinal_exvivo.label)(.*)$', val[0]):
                datatemp[i][0] = re.sub(r'^(.*)(entorhinal_exvivo)(.*)$', r'\2', val[0])
            for lesZ in lesmesures:
                if datatemp[i][0] + "_" + tableFile[:1].upper() + lesZ in ledata[0]:
                    # verify if encounter same structure with different value
                    for j, val1 in enumerate(ledata[0]):
                        if ledata[0][j] == datatemp[i][0] + "_" + tableFile[:1].upper() + lesZ:
                            if lesZ == 'S':
                                if ledata[index_patient][j] != datatemp[i][2] and ledata[index_patient][j] != '':
                                    affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                                ledata[index_patient][j] = datatemp[i][2]
                            if lesZ == 'V':
                                if ledata[index_patient][j] != datatemp[i][3] and ledata[index_patient][j] != '':
                                    affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                                ledata[index_patient][j] = datatemp[i][3]
                            if lesZ == 'T':
                                if ledata[index_patient][j] != datatemp[i][4] and ledata[index_patient][j] != '':
                                    affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                                ledata[index_patient][j] = datatemp[i][4]
                else:
                    #Adding column to array
                    ledata = [x + [''] for x in ledata]
                    ledata[0][len(ledata[0]) - 1] = datatemp[i][0] + "_" + tableFile[:1].upper() + lesZ #tableFile[:1] + "_" + lesZ + "_" + datatemp[i][0]
                    if lesZ == 'S':
                        ledata[index_patient][len(ledata[0])-1] = datatemp[i][2]
                    if lesZ == 'V':
                        ledata[index_patient][len(ledata[0])-1] = datatemp[i][3]
                    if lesZ == 'T':
                        ledata[index_patient][len(ledata[0])-1] = datatemp[i][4]

    return ledata
##########################################################################################
def parse_aseg(lexml, lefolder, patient_name, tableFile, ledata, VolumeOnly):

    filepath = os.path.join(lefolder, patient_name, "stats", tableFile)

    if os.path.isfile(filepath) is False:
        return ledata

    # find patient's line
    for p, val in enumerate(ledata):
        for q, lav in enumerate(val):
            if lav == patient_name:
                index_patient = p

    # add data from stats files
    ventricles_log = CCsum = 0
    datatemp = medics.createTuple(filepath)
    for i, val in enumerate(datatemp):
        ### MEASURE
        if val[0].find("Measure") >= 0:
            if (val[1] == "eTIV") or val[1].find("hCortexVol") >= 0 or val[1] == "SubCortGrayVol" or (VolumeOnly is True and val[1] == "BrainSegVolNotVent") or (VolumeOnly is True and val[1] == "TotalGrayVol"):
                #need to transform certain names for uniformity
                if re.search(r'^(.*)(hCortexVol)(.*)$', val[1]):
                    datatemp[i][1] = re.sub(r'^(.*)(Cortex)(.*)$', r'\2', val[1]) + "_" + re.sub(r'^([lr])(h)(Cortex)(.*)$', r'\1', val[1]).upper() + "V"
                if datatemp[i][1] in ledata[0]:
                    for j, val1 in enumerate(ledata[0]):
                        if ledata[0][j] == datatemp[i][1]:
                            if ledata[index_patient][j] != datatemp[i][3] and ledata[index_patient][j] != '':
                                affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                            ledata[index_patient][j] = datatemp[i][3]
                else:
                    ledata = [x + [''] for x in ledata]
                    ledata[0][len(ledata[0]) - 1] = datatemp[i][1]
                    #(" Adding \"" + str(datatemp[i][1]) + "\" column to array")
                    ledata[index_patient][len(ledata[0])-1] = datatemp[i][3]
        ### STRUCTURES
        if val[0][:1] != '#':
            #exceptions:
            if datatemp[i][4] != 'CSF' and datatemp[i][4].find("erebellum") == -1 and datatemp[i][4].find("vessel") == -1 and datatemp[i][4].find("choroid") == -1 and datatemp[i][4].find("WM-") == -1 and datatemp[i][4].find("Optic") == -1:
                #Sum section:
                if datatemp[i][4].find("Vent") >= 0 and datatemp[i][4].find("Ventral") == -1:
                    ventricles_log = ventricles_log + float(datatemp[i][3])
                if datatemp[i][4].find("CC_") >= 0:
                    CCsum = CCsum + float(datatemp[i][3])
                if datatemp[i][4].find("CC_") == -1 and datatemp[i][4].find("5th") == -1:
                    if datatemp[i][4] in ledata[0]:
                        for j, val1 in enumerate(ledata[0]):
                            if ledata[0][j] == datatemp[i][4]:
                                if ledata[index_patient][j] != datatemp[i][3] and ledata[index_patient][j] != '':
                                    affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                                ledata[index_patient][j] = datatemp[i][3]
                    else:
                        ledata = [x + [''] for x in ledata]
                        ledata[0][len(ledata[0]) - 1] = datatemp[i][4]
                        ledata[index_patient][len(ledata[0])-1] = datatemp[i][3]
    #add calculated columns
    if "ventricles_log" in ledata[0]:
        for j, val1 in enumerate(ledata[0]):
            if ledata[0][j] == "ventricles_log":
                if ledata[index_patient][j] != ventricles_log and ledata[index_patient][j] != '':
                    affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                ledata[index_patient][j] = ventricles_log
    else:
        ledata = [x + [''] for x in ledata]
        ledata[0][len(ledata[0]) - 1] = "ventricles_log"
        ledata[index_patient][len(ledata[0])-1] = ventricles_log
    if "CCsum" in ledata[0]:
        for j, val1 in enumerate(ledata[0]):
            if ledata[0][j] == "CCsum":
                if ledata[index_patient][j] != CCsum and ledata[index_patient][j] != '':
                    affiche_warning(lexml, "same", " (" + ledata[0][j] + ")")
                ledata[index_patient][j] = CCsum
    else:
        ledata = [x + [''] for x in ledata]
        ledata[0][len(ledata[0]) - 1] = "CCsum"
        ledata[index_patient][len(ledata[0])-1] = CCsum

    return ledata
##########################################################################################
def remove_column(ledata):
    index = ledata[0].index('eTIV')
    for i, val in enumerate(ledata):
        del val[index]
    for j, val1 in enumerate(ledata[0]):
        if val1.find("_log") != -1:
            ledata[0][j] = val1.replace("_log", "")

##########################################################################################
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    py3 = sys.version_info[0] > 2
    if py3:
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()
##########################################################################################
def verify_args(args, lexml):
    verify_args = False
    
    if not os.path.isfile(args.input_csv):
        affiche_erreur(lexml, "miss")
    if not args.input_csv.strip().lower().endswith('.csv'):
        affiche_erreur(lexml, "notcsv")
    if not os.path.isdir(args.subjects_dir):
        affiche_erreur(lexml, "notdir")
    verify_args = True
    return verify_args
    
##########################################################################################
def getScoreZ(args, lexml):
    csvpath = ""
    efface = False
    getScoreZ = " !Oops! There was an error."

    if verify_args(args, lexml):
        VolumeOnly = False
        if args.volumes:
            VolumeOnly = True
        
        lestables = tables[normes.index([args.atlas.upper()])]
        lefilenorme = str(normes[normes.index([args.atlas.upper()])][0]) + '.csv'
        lefilenorme = os.path.join(os.path.dirname(os.path.realpath(__file__)), lefilenorme)
        lefile = args.input_csv
        lefolder = args.subjects_dir
        
        printProgressBar(0, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
        
        ledata = medics.createTuple(lefile)###->READ CSV
    
        ###->READ STATS IN FOLDERS
        ACounter = 0
        index_patient = None
        ###search patient column from csv
        for i, val in enumerate(ledata[0]):
            if (re.search(r'^(.*)(patient|subject)(.*)(id)(.*)$', ledata[0][i], re.IGNORECASE)) or (ledata[0][i].lower().strip().replace('"','') == 'id'):
                index_patient = i
                ACounter += 1
        if index_patient is None:
            affiche_erreur(lexml, "id")
            return
        if ACounter > 1:
            affiche_erreur(lexml, "ids")
            return
        #start at second line not including matrix header (first line)
        found_one = False
        for i, val in list(enumerate(ledata))[1:]:
            patient_name = val[index_patient].replace('"','')
            # patient's folder is "rootdir/patient_id/stats/files.stats"
            d = os.path.join(lefolder, patient_name, 'stats')
            # if dir stats does not exist, continue
            if not os.path.isdir(d):
                continue #next subject if no stats folder
            else:
                found_one = True
            for i, latable in enumerate(lestables):
                if latable.find("aseg") == -1:
                    try:
                        ledata = parse_aparc(lexml, lefolder, patient_name, latable, ledata)  # ledata pass byref
                    except Exception as e:
                        affiche_erreur(lexml, "nothing", "ERROR %s on aparc file %s for patient %s." % (e.__class__.__name__, latable, patient_name))
                        #return
                else:
                    try:
                        ledata = parse_aseg(lexml, lefolder, patient_name, latable, ledata, VolumeOnly)
                    except Exception as e:
                        affiche_erreur(lexml, "nothing", "ERROR %s on aseg file %s for patient %s." % (e.__class__.__name__, latable, patient_name))
                        #return    
        if found_one == False:
            affiche_erreur(lexml, "nofolder")
            return
        #load norme file
        lenorme = []
        with open(lefilenorme) as csvfile:
            reader = csv.reader(csvfile, dialect='excel')
            for x, y in enumerate(reader):
                lenorme.append(y)
    
        #get formula
        larowformule = [row for row in lenorme if 'NORME' in row[0]]
        laformule = larowformule[0][2]
    
        #loop volumes
        lesindex=[];lesindexDK=[];lesindexASEG=[]
        BCounter=0;lindexgenre=-1;lindexage=-1;lindexmanufac=-1;lindexmagnet=-1;lindexetiv=-1
        for i, val in enumerate(ledata[0]): # header
            ##look for particuliar values
             # gender
            lindexgenre = [k for k, x in enumerate(ledata[0]) if re.search(r'^(.*)(gen|sex)(.*)$', x, re.IGNORECASE) ]
            if len(lindexgenre) > 1:
                affiche_erreur(lexml, "many", " gender.")
                return
            elif len(lindexgenre) == 0:
                affiche_erreur(lexml, "none", " gender.")
                return
            else:
                lindexgenre = lindexgenre[0]
             # age
            lindexage = [k for k, x in enumerate(ledata[0]) if re.search(r'^(.*)(age)(.*)$', x, re.IGNORECASE) ]
            if len(lindexage) > 1:
                affiche_erreur(lexml, "many", " age.")
                return
            elif len(lindexage) == 0:
                affiche_erreur(lexml, "none", " age.")
                return
            else:
                lindexage = lindexage[0]
             # manufacturer
            lindexmanufac = [k for k, x in enumerate(ledata[0]) if re.search(r'^(.*)(manufa)(.*)$', x, re.IGNORECASE) ]
            if len(lindexmanufac) > 1:
                affiche_erreur(lexml, "many", " manufacturer.")
                return
            elif len(lindexmanufac) == 0:
                affiche_erreur(lexml, "none", " manufacturer.")
                return
            else:
                lindexmanufac = lindexmanufac[0]
             # magnetic feild
            lindexmagnet = [k for k, x in enumerate(ledata[0]) if re.search(r'^(.*)(magn|fiel|champ|forc|streng)(.*)$', x, re.IGNORECASE) ]
            if len(lindexmagnet) > 1:
                affiche_erreur(lexml, "many", " magnetic field strength.")
                return
            elif len(lindexmagnet) == 0:
                affiche_erreur(lexml, "none", " magnetic field strength.")
                return
            else:
                lindexmagnet = lindexmagnet[0]
             # eTIV
            lindexetiv = [k for k, x in enumerate(ledata[0]) if re.search(r'^(.*)(eTIV)(.*)$', x, re.IGNORECASE) ] ## programmatically insert
            lindexetiv = lindexetiv[0]
            ##verify if all is there
            if lindexgenre==-1 or lindexage==-1 or lindexmanufac==-1 or lindexmagnet==-1 or lindexetiv==-1:
                affiche_erreur(lexml, "wrongCSV")
                return
            else:
                lesindex = [index_patient, lindexgenre, lindexage, lindexmanufac, lindexmagnet, lindexetiv]
            ##formula transformation
            if i not in [index_patient, lindexgenre, lindexage, lindexmanufac, lindexmagnet, lindexetiv]:
                if re.search(r'^(.*)(\_[LR][SVT])$', val):
                    lesindexDK.append(i)
                else:
                    lesindexASEG.append(i)
                if VolumeOnly is False:
                    BCounter = BCounter + 1
                    for j in range(1, len(ledata) ):#check all value from a column, for each line
                        if j == 1:#get structure define constantes from norme, one time only
                            lastructure = [row for row in lenorme if re.sub(r'[^0-9a-zA-Z]+', '', val.lower()) in re.sub(r'[^0-9a-zA-Z]+', '', row[3].lower())]
                        if BCounter == 1 and j ==1:# build complete formula
                            lastructureDK = [row for row in lenorme if (row[0] == "eTIVc" or row[0] == "agec") and row[4].strip() != "SUBCOR"]
                            lastructureASEG = [row for row in lenorme if (row[0] == "eTIVc" or row[0] == "agec") and row[4].strip() == "SUBCOR"]
                            for k, v in enumerate(lastructure):
                                laformule = re.sub(r'\b' + v[0] + r'\b', v[2], laformule)
                        levolume = ledata[j][i]
                        if levolume is None or len(str(levolume)) == 0: #volume of structure missing because no stats file
                            levolume = 0
                        laformule_temp = laformule
                        if len(lastructure) > 0:
                            if re.search(r'^(.*)(_log)$', lastructure[0][3], re.IGNORECASE):
                                laformule_temp = laformule_temp.replace("[volume]", "log([volume], 10)")
                        laformule_temp = laformule_temp.replace("[volume]", str(levolume))
                        if ledata[j][lindexgenre] == 'M':
                            laformule_temp = laformule_temp.replace("[gender]", "1")
                        elif ledata[j][lindexgenre] == 'F':
                            laformule_temp = laformule_temp.replace("[gender]", "0")
                        if round(float(ledata[j][lindexmagnet]),1) == 1.5:
                            laformule_temp = laformule_temp.replace("[magnetic_field_strength]", "1")
                        elif round(int(ledata[j][lindexmagnet])) == 3:
                            laformule_temp = laformule_temp.replace("[magnetic_field_strength]", "0")
                        if re.search(r'^(.*)(GE)(.*)$', str(ledata[j][lindexmanufac])): #, re.IGNORECASE)
                            laformule_temp = laformule_temp.replace("G_[modality_manuf_id]", "1")
                        else:
                            laformule_temp = laformule_temp.replace("G_[modality_manuf_id]", "0")
                        if re.search(r'^(.*)(phil)(.*)$', str(ledata[j][lindexmanufac]), re.IGNORECASE):
                            laformule_temp = laformule_temp.replace("P_[modality_manuf_id]", "1")
                        else:
                            laformule_temp = laformule_temp.replace("P_[modality_manuf_id]", "0")
                        for m, n in enumerate(lastructure):
                            laformule_temp = re.sub(r'\b' + n[0] + r'\b', n[1], laformule_temp)
                        if re.search(r'^(.*)(_L|_R)([VTS])(.*)$', val):
                            for k, v in enumerate(lastructureDK):
                                laformule_temp = re.sub(r'\b' + v[0] + r'\b', v[2], laformule_temp)
                            for o, p in enumerate(lastructureDK):
                                laformule_temp = re.sub(r'\b' + p[0] + r'\b', p[1], laformule_temp)
                        else:
                            for k, v in enumerate(lastructureASEG):
                                laformule_temp = re.sub(r'\b' + v[0] + r'\b', v[2], laformule_temp)
                            for o, p in enumerate(lastructureASEG):
                                laformule_temp = re.sub(r'\b' + p[0] + r'\b', p[1], laformule_temp)
                        laformule_temp = laformule_temp.replace("[patient_age]", str(ledata[j][lindexage]))
                        laformule_temp = laformule_temp.replace("[eTIV]", str(ledata[j][lindexetiv]))
    
                        laformule_temp = laformule_temp.replace("Z=", "")
    
                        try:
                            if levolume != 0:
                                leZ = str(eval(laformule_temp))
                                ledata[j][i] = leZ
                            else:
                                ledata[j][i] = "-999"
                        except NameError:
                            ledata[j][i] = "-999"
            printProgressBar(int((float(i)/(len(ledata[0])-1))*100), 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
    
        if int((float(i)/(len(ledata[0])-1))*100) == 100: #progres["value"] == 100:
            outdir = '.'
            outfile = 'results_' + str(normes[normes.index([args.atlas.upper()])][0]) + "_" + time.strftime("%Y%m%d-%H%M%S") + '.csv'
            if args.output_csv is not None: # and os.path.isdir(os.path.dirname(os.path.abspath(args.output_csv))):
                if args.output_csv.strip().lower().endswith('.csv'):#csv was given
                    outdir2, outfile2 = os.path.split(args.output_csv)
                    if os.path.isdir(outdir2):#path valid continue verification
                        if os.path.isfile(os.path.join(outdir2, outfile2)):#file exist 
                            if medics.query_yes_no(lexml.getElementsByTagName("query_yes_no")[0].childNodes[0].nodeValue.strip(), None):#asking user for replace file
                                efface = True
                                outfile = outfile2
                                outdir = outdir2
                            else:#user say no
                                affiche_warning(lexml, "dont_replace")
                        else:#file dont exist,create it
                            outfile = outfile2
                            outdir = outdir2
                    else:#path part invalid
                        affiche_warning(lexml, "output_invalid")
                else:#not a csv
                    affiche_warning(lexml, "output_invalid")
            lecsv = outfile
            csvpath = os.path.join(outdir, lecsv)
            ledata = medics.sort_csv(ledata, lesindex, lesindexDK, lesindexASEG)
            if VolumeOnly is False:
                remove_column(ledata)
            file_save(ledata, csvpath, args, efface)
        else:
            affiche_erreur(lexml, "notdone")
    if csvpath != "":
        getScoreZ = csvpath
    return getScoreZ

##########################################################################################
