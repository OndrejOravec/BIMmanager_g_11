
<details>
  <summary>A2a. About our group</summary>
   How much do agree with this statement? : "I am confident coding in Python"
   
  ### Group 11 - Managers
  - *Ondrej* : 2
  - *Magnus* : 3

  ###  Group 14 - Analysts
  - *Jannik* : 1
  - *Mathushan* : 2

  ###  Group 15 - Analysts
  - *Zohaib* : 1
  - *Mikael* : 2


 ### Total Score: 11

</details>
  
---
<details>
  <summary>A2b. Identify claim</summary>

  ### Group 14 - Claim
  - **Claim:** The amount of technical installations and AHU-units used in the ventilation system, which aligns with the design and regulatory requirements.
  - **Report Reference:** "CES_BLD_24_0_6_MEP" (p. 8)
  - **Description of claim we wish to check** We are verifying the claim that the ventilation system, including AHUs and technical installations (like ducts, pipes, etc.), complies with the building regulations and design-standards. This involves checking the amount of equipment, their dimensions, and the capacity of airflow too.
  - **Justification of selection of our claim** Ventilation is essential for ensuring good air quality in the building, and any inconsistencies could impact occupant health or energy-efficiency.

  ### Group 15 - Claim
  - **Claim:** We wil try to find U-Value. The U-Value of a material or structure significantly impacts the amount of
  daylight allowed through a building envelope,affecting thermal performance and energy efficiency
  - **Report Reference:** We can find this in the "CES_BLD_24_0_6_MEP" (page 15)
  - **Description of claim we wish to check** We are investigating whether the reported U-Value for certain materials (likely glass or windows)
  optimally balances thermal insulation and daylight penetration, improving energy efficiency and occupant comfort.
  - **Justification of selection of our claim** This claim is crucial as it touches on both energy efficiency and building comfort.
  The U-Value is a measure of heat loss, and ensuring proper daylight entry without compromising
  insulation is key to designing sustainable and energy-efficient buildings.



</details>

---
<details>
  <summary>A2c. Use Case</summary>

  ### Group 14 - Claim
  - **How and when we check this claim?** We check the claim by comparing the amount of ventilation components (e.g. AHU, pipes, etc.) found in the MEP IFC-model with those specified in the MEP-design report. This check will occur in the next assignment during the design validation phase and right before installation.
  - **What information does this claim rely on?** The claim relies on the components of the ventilation in the BlenderBIM-model, their quantities and properties. This includes the AHUs, ducts and the flow rates supplied by mostly the MEP-report of the ventilation 
  - **What BIM purpose is required?** The BIM purpose is ventilation and technical installations

  - **BPMN drawing:**   
  1. First we extract ventilation data from IFC Model
  2. The we validate against MEP-report
  3. Subsequently, we calculate ventilation needs
  4. And finally, we generate validation report.

  ### Group 15 - Claim
  - **How and when we check this claim?** We will check the claim by creating a Python script within Blender to analyze the U-Value's impact on daylight performance in our building
  - **What information does this claim rely on?** Material properties, particularly the U-Value of windows or glazing systems (thermal transmittance).
  Daylight transmittance data, Visible Light Transmittance or Solar Heat Gain Coefficient.
  standards and codes which is cited in the report ("CES_BLD_24_0_6_MEP" (page 15))
  - **What BIM purpose is required?** The BIM purpose is energy and lighting performance analysis, focusing on daylight.We will use BIM to simulate the building design based on energy efficiency and daylight.
 We will analyze material choices (glazing) by integrating U-Value calculations with daylight simulations.
 And by using python to research our assignment
  - **BPMN drawing:** 

  </details>

---
<details>
  <summary>A2d. Scope the Use Case</summary>

  - **Identify where a new script/fucntion/tool is needed and highlight this in BPMN diagram** 
  ### Group 14 

 1. In first step a script or tool is required to systamize the extraction of ventilation components. This will access and list the required data from the model effectively.
 2. A function is needed here to compare the extracted data from the IFC-model with the MEP-report. The function would guarantee that quantities, dimensions and flow rates match the specifications for design and regulations.
 3. A sript would also include calculations for airflow based on the size of the room and the amount of occupants, which could be incorporated into the validation tool or done separately.



  </details>

---
<details>
  <summary>A2e. Tool Idea</summary>



 ### Group 14
  - **Describe idea of your OpenBIM ifcOpenShell Tool**   The tool will focus on extracting ventilation and technical installation data from the IFC-file, here including ducts, pipes, and AHUs, etc. It will also systemaize checks for regulatory compliance, perform calculations for required airflow per room, and them generate a report showing if the design meets its requirements.

  - **Business and Societal value:** The tool ensures that the ventilation system meets the necessary standards, reducing the risk of bad indoor air quality and don't go against the regulations. This will lead to healthier building environments and reduce costs associated with design errors.

  - **Summarizing BPMN diagram:**  The diagram shows the process from starting from extracting data to performing validation to then calculating ventilation requirements to finally generating the report.

 ### Group 15
 - **Describe idea of your OpenBIM ifcOpenShell Tool** The idea behind our  OpenBIM ifcOpenShell Tool is to provide an open-source solution for working with  IFC in the BIM environment. It allows users to create, modify, and analyze IFC files without being tied to proprietary software. Our tool is designed to help professionals  by ensuring that BIM data can be shared and used across different platforms.
  - **Business and Societal value:** Business Value: Cost savings, interoperability, process automation, and regulatory compliance.
 Societal Value: Promotes sustainability, knowledge sharing, and increases accessibility to BIM  tools for smaller firms and educational institutions.
  - **Summarizing BPMN diagram:**
  
  </details>

---
<details>
  <summary>A2f. Information requirements</summary>
 
  ### Group 14
 - **Identification of required information from model**  For ventilation, the required information is:
 AHUs (IfcBuildingElementProxy)
 Ducts and pipes (IfcFlowSegment)
 Valves, dampers and other technical installations (IfcFlowController)
 Relevant geometric and performance properties, including flow rates and capacities.



 ### Group 15
  - **Identification of required information from model** To calculate the U-value of a window, you need to know the thermal conductivity of the materials (glass, frame, and gas between panes), the number of glass layers (single, double, or triple glazing), the thickness of the glass and gaps between panes, and the type of gas used in the cavity (e.g., air, argon).
 Additionally, the presence of Low-E coatings, the material of the window frame (wood, aluminum, PVC),
 and the type of spacer bars (e.g., aluminum or warm-edge) also affect the U-value. 
  </details>

---
<details>
  <summary>A2g. Identify appropriate software licence</summary>

  </details>

---
