#pip install ifcopenshell

#1TO UPDATE INFORMATION FROM GROUPS RUN COMMAND:
#git submodule update --rebase --remote --recursive

#2. TO RUNNS SCIPT, REMOVE # FROM CORRESPODNING LINE OF SCRIPT POINTING INTO UR DIRECTORY 

import ifcopenshell
print("Imported ifcopenshell")

from external.BIManalyst_g_14.rules import AHURule
from external.BIManalyst_g_15.rules import windowRule

print("Loading MEP-model...")
#MEP model:
model_MEP = ifcopenshell.open("C:\\Users\\magnu\\OneDrive - Danmarks Tekniske Universitet\\DTU\\Kandidat\\Tredje semester\\41934 Advanced Building Information Modeling\\IFC_Models\\CES_BLD_24_06_MEP.IFC")
print("Loading ARC-model...")
#Architectural model:
model_ARC = ifcopenshell.open("C:\\Users\\magnu\\OneDrive - Danmarks Tekniske Universitet\\DTU\\Kandidat\\Tredje semester\\41934 Advanced Building Information Modeling\\IFC_Models\\CES_BLD_24_06_ARC.IFC")
print("Model loaded.")

#MEP model Ondrej :
#model = ifcopenshell.open("C:\\Users\\ondro\\Desktop\\skola\\DTU MSc\\3year\\Advanced BIM\\BIM models\\C:\Users\\ondro\\Desktop\\skola\\DTU MSc\\3year\\Advanced BIM\\BIM models\\CES_BLD_24_06_MEP.IFC")

#Architectural model Ondrej:
#model = ifcopenshell.open("C:\\Users\\ondro\\Desktop\\skola\\DTU MSc\\3year\\Advanced BIM\\BIM models\\C:\\Users\\ondro\\Desktop\\skola\\DTU MSc\\3year\\Advanced BIM\\BIM models\\CES_BLD_24_06_ARC.IFC")
print("Model loaded.")

#Checking MEP-model loading correctly
if model_MEP is None:
    print("Failed to load MEP model.")
else:
    print("MEP model loaded successfully.")


#Checking ARC-model loading correctly
if model_ARC is None:
    print("Failed to load ARC model.")
else:
    print("ARC model loaded successfully.")

#Script begins
print("Script started")

#Group 14 (MEP-Model)
AHUResult = AHURule.checkRule(model_MEP)
print("AHU rule executed")
print("AHU result:", AHUResult)

#Group 15 (ARC-Model)
windowResult = windowRule.checkRule(model_ARC)
print("Window rule executed")
print("Window result:", windowResult)
