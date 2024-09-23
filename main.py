#pip install ifcopenshell

#TO UPDATE INFORMATION FROM GROUPS RUN COMMAND:
#git submodule update --rebase --remote --recursive

import ifcopenshell
print("Imported ifcopenshell")

from external.BIManalyst_g_15.rules import windowRule

print("Loading model...")
#MEP model:
#model = ifcopenshell.open("C:\\Users\\magnu\\OneDrive - Danmarks Tekniske Universitet\\DTU\\Kandidat\\Tredje semester\\41934 Advanced Building Information Modeling\\IFC_Models\\CES_BLD_24_06_MEP.IFC")

#Architectural model:
model = ifcopenshell.open("C:\\Users\\magnu\\OneDrive - Danmarks Tekniske Universitet\\DTU\\Kandidat\\Tredje semester\\41934 Advanced Building Information Modeling\\IFC_Models\\CES_BLD_24_06_ARC.IFC")
print("Model loaded.")

#Checking model loading correctly
if model is None:
    print("Failed to load IFC model.")
else:
    print("IFC model loaded successfully.")

#Script begins
print("Script started")
windowResult = windowRule.checkRule(model)
print("Window rule executed")
print("Window result:", windowResult)
