This document serves as Assignment A2: Use Case. We are submitting it alongside the A3 assignment to address missing information that could not be updated earlier since we as managers, decided to develop our own tool after the  A2 submission.

This document serves as Assignment A2: Use Case. It is being submitted alongside the A3 assignment to address missing information that could not be updated earlier. As managers, we decided to develop our own tool after the A2 submission.

## A2b. Identify Claim

  - **Claim:**  
    To verify if the Reverberation Time (T) of different rooms complies with acoustic recommendations.

  - **Report Reference:**  
    "CES_BLD_24_0_6_MEP" (p. 21)

  - **Description of the Claim:**  
    The idea is to develop a tool to verify whether the acoustic environment of different kinds of rooms (e.g., meeting rooms, small offices) complies with acoustic criteria for Reverberation Time (T).

  - **Justification for Selecting this Claim:**  
    Reverberation Time (T) is a key parameter in room acoustics, playing a crucial role in creating a suitable indoor environment within buildings.

## A2c. Use Case

  - **How and When We Check this Claim:**  
    By extracting room volumes (V) and surface areas (S) with their corresponding absorption coefficients (α) for specific rooms, and performing Reverberation Time (T) calculations using Sabine's equation. The results will be compared with acoustic recommendations for meeting rooms and offices.

  - **Information the Claim Relies On:**  
    Accurate extraction of room volumes and their boundaries (e.g., walls and ceilings). Differentiating between walls with different finishing layers is crucial since they have varying sound absorption coefficients, directly impacting Reverberation Time calculations.

  - **BIM Purpose Required:**  
    All five BIM purposes will be included: Gather, Generate, Analyse, Communicate, and Realize.

  - **BPMN Drawing:**  
    1. Load the model.  
    2. Identify room boundaries.  
    3. Calculate areas.  
    4. Identify sound absorption coefficients.  
    5. Determine the analysis range.  
    6. Generate results and compare them with acoustic recommendations.

## A2d. Scope the Use Case

  - **Identify the Need for a New Script/Function/Tool:**  
    Our script is mainly required in the "Room boundaries definition" part since the provided IFC model does not have room boundaries defined via the corresponding function in the specific BIM software where the model was created.  

    Additionally, the script provides a tool to determine the absorption coefficients of different surfaces if the sound absorption coefficients are not defined in the IFC model.  

    Furthermore, the script filters and considers only specific (regular) room shapes, as Sabine's formula for reverberation time calculations is applicable to regular room shapes.

## A2e. Tool Idea

  - **Description of the OpenBIM ifcOpenShell Tool:**  
    The tool enables fast extraction and assessment of Reverberation Time, enhancing interdisciplinary workflows among professionals at different stages of project planning.

  - **Business and Societal Value:**  
    This tool helps prevent poor acoustic indoor environments. Evidence suggests that a bad acoustic environment can have adverse effects on human health and work productivity.

  - **Summary of BPMN Diagram:**  
    The diagram represents the workflow of our script, covering data extraction, assessment, subsequent calculations, and evaluation against standard recommendations.

## A2f. Information Requirements

  - **Required Information from the Model:**  
    - Walls  
    - Ceilings  
    - Curtain Walls  
    - Windows  
    - Floors

## A2g. Identify Appropriate Software License

  - **Software License:**  
    No license needed as the 3D-modelling program used "Blender" is open-software and all the coding has been done in VSCode using Python which is also open-software.

