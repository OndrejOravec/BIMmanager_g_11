This document serves as Assignment A2: Use Case. We are submitting it alongside the A3 assignment to address missing information that could not be updated earlier since we as managers, we decided to develop our own tool after the  A2 submission.

---
<details>
  <summary>A2b. Identify claim</summary>

  - **Claim:** To verify if  Reverberation Time T of different rooms comply with acoustic recommendations.
  - **Report Reference:** "CES_BLD_24_0_6_MEP" (p. 21)
  - **Description of claim we wish to check** The idea is to develop a tool to verify if the acoustic environment of different kinds of rooms (meeting rooms, small offices) comply with acoustic criteria for Reverberation Time T.
  - **Justification of selection of our claim** Reverberation Time T is a key parameter in room acoustics, playing a crucial role in creating a suitable indoor environment within buildings.

</details>

---
<details>
  <summary>A2c. Use Case</summary>

  - **How and when we check this claim?** This would be done by extracting rom volumes V and different surface areas S with their corresponding absorption coefficient α of specific rooms and performing Reverberation calculation T using Sabine equation, consequently it would be compared with Reverberation Time recommendations for meeting rooms and offices.
  - **What information does this claim rely on?** It depends on the accurate extraction of room volumes and their boundaries, such as walls and ceilings. Additionally, distinguishing between walls with different finishing layers is crucial, as they have varying sound absorption coefficients that directly impact the calculation of Reverberation Time.
  - **What BIM purpose is required?** All 5 BIM purposes will be included (Gather, Generate, Analyse, Communicate, Realize).

  - **BPMN drawing:**   
  1. Loading of model.
  2. Room boundaries identification 
  3. Area calculation
  5. Sound absorption coefficient identification
  6. Analysis range determination
  7. Generation of result and subsequent comparison with acoustic recommendation


  </details>

---
<details>
  <summary>A2d. Scope the Use Case</summary>

  - **Identify where a new script/fucntion/tool is needed and highlight this in BPMN diagram** 

 1. In first step a script or tool is required to systamize the extraction of ventilation components. This will access and list the required data from the model effectively.
 2. A function is needed here to compare the extracted data from the IFC-model with the MEP-report. The function would guarantee that quantities, dimensions and flow rates match the specifications for design and regulations.
 3. A sript would also include calculations for airflow based on the size of the room and the amount of occupants, which could be incorporated into the validation tool or done separately.



  </details>

---
<details>
  <summary>A2e. Tool Idea</summary>

  - **Describe idea of your OpenBIM ifcOpenShell Tool**   Tool serves for fast extraction and assesment of Reverberation Time to enchance inter-disciplinary workflow between proffesions throughout different stages of project planning.

  - **Business and Societal value:** It has a value in preventing bad acoustic indoor environment. There is a evidence how bad acoustic environment can have adverse effect on human health and work productivity.

  - **Summarizing BPMN diagram:**  Diagram demonstrates representation of workflow of our script. From extraction of data, assesment, subsequent calculation and evaluation in relation to standart recommendations.

 
  </details>

---
<details>
  <summary>A2f. Information requirements</summary>
 
 - **Identification of required information from model**  
 
 Walls 
 
 Ceilings
 
 CurtainWalls
 
 Windows
 
 Floors

  </details>

---
<details>
  <summary>A2g. Identify appropriate software licence</summary>

  </details>

---
