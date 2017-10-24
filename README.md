# mNormsFS53
Normative morphometric data calculator for FreeSurfer 5.3
#################################### INSTRUCTIONS #####################################

@2017 MEDICS LABORATORY - CERVO RESEARCH CENTER - UNIVERSITE LAVAL

Normative morphometric data calculator for FreeSurfer 5.3 - Version 1.0

The authors take no responsibility for the use of this script or its derivatives.
These normative data are not for diagnostic purposes.

These normative values are aimed to be used with FreeSurfer version 5.3 with default parameters.
All values were produced using the “recon-all -all” command without any flag option.
Normative values are Z scores with a mean of 0 and a standard deviation of 1.
For cortical values, you need to specify the atlas (Desikan-Killiany (DK) or Desikan-Killiany-Tourville (DKT)
Values for subcortical and ex-vivo atlases are generated by default.


>>> References

 Please cite and refer to the following publications for details:

 Potvin et al. (2017). Normative morphometric data for cerebral cortical areas over the lifetime of the adult human brain. NeuroImage, 156, 315-339.
 Potvin et al. (2017). FreeSurfer cortical normative data for adults using Desikan-Killiany-Tourville and Ex vivo protocols. NeuroImage, 156, 43-64.
 Potvin et al. (2016). Normative data for subcortical regional volumes over the lifetime of the adult human brain. NeuroImage, 137, 9-20.


>>> Script

 Extract the downloaded package. 
 Run the python script (mNormsFS53.py) from a terminal

 usage: python mNormsFS53.py [-h] -s <SUBJECTS_DIR> -i <INPUT_CSV> -a <DK|DKT> [-o <OUTPUT_CSV>]

 optional arguments:
   -h, --help       show this help message and exit
   -o               CSV file to save the results of this tool. If omitted, file
                    will be saved in current directory.
     
 required arguments:
   -s               The path to the directory containing all the FreeSurfer
                    subjects folders.
   -i               CSV file containing subjects id (as in FreeSurfer’s subject
                    directory), sex (M/F), age, manufacturer (GE/Philips/Siemens),
                    and magnetic field strength (1.5/3). 
                    For an example, see "Example/intrant_example.csv"

   -a {dk,dkt}      Choose between DK or DKT atlas.

 A complete example with a CSV file and FreeSurfer output is provided (see Example/). From the folder mNormsFS53/, this command should produce normative data for the example:

 python mNormsFS53.py -s Example/FreeSurfer_dir -i Example/intrant_example.csv -a DKT -o ./my_normative_values.csv


>>> Cortical atlases (DK, DKT, and Ex vivo)

 Each region Z score is identified with a suffix of two letters corresponding to Left (L) or Right (R) hemisphere followed by Surface (S),
 Thickness (T), or Volume (V). These regions correspond to SurfArea, ThickAvg, or GrayVol within the following FreeSurfer stats files:
 lh.aparc.DKTatlas40.stats
 lh.aparc.stats
 lh.BA.stats
 lh.entorhinal_exvivo.stats
 rh.aparc.DKTatlas40.stats
 rh.aparc.stats
 rh.BA.stats
 rh.entorhinal_exvivo.stats 

 Cortex surface = White Surface Total Area 
 Cortex thickness = Mean Thickness
 Cortex volume = Hemisphere cortical gray matter volume (from aseg.stats)


>>> Subcortical atlas (aseg.stats)

 Z score names are identical to those within the file except:
 CCsum = sum of the corpus callosum divisions
 ventricles = sum of all ventricles

################################################################################################################################
