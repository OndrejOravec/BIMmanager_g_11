#pip install ifcopenshell
import ifcopenshell
print("Imported ifcopenshell")

from external.BIManalyst_g_14.rules import windowRule
from external.BIManalyst_g_15.rules import doorRule

print("Loading model...")
#MEP model (Magnus)
#model = ifcopenshell.open("C:\\Users\\magnu\\OneDrive - Danmarks Tekniske Universitet\\DTU\\Kandidat\\Tredje semester\\41934 Advanced Building Information Modeling\\IFC_Models\\CES_BLD_24_06_MEP.IFC")

#Architectural model (Magnus):
#model = ifcopenshell.open("C:\\Users\\magnu\\OneDrive - Danmarks Tekniske Universitet\\DTU\\Kandidat\\Tredje semester\\41934 Advanced Building Information Modeling\\IFC_Models\\CES_BLD_24_06_ARC.IFC")

#MEP model (Ondrej)
#model = ifcopenshell.open("C:\\Users\\ondro\\Desktop\\skola\\DTU MSc\\3year\\Advanced BIM\\BIM models\\CES_BLD_24_06_MEP.IFC")

#Architectural model (Ondrej):
model = ifcopenshell.open("C:\\Users\\ondro\\Desktop\\skola\\DTU MSc\\3year\\Advanced BIM\\BIM models\\CES_BLD_24_06_ARC.IFC")


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
doorResult = doorRule.checkRule(model)
print("Door rule executed")
print("Window result:", windowResult)
print("Door result:", doorResult)