# Important

  As we have chosen to transition from managers to develop an independent tool, we have completed the A2-assignment for our project and uploaded it as "Supplementary A2.dm" in this repository. Additionally, the BPMN diagram is available as a `.svg` file in this repository. Furthermore, the entire script is located in `main.py` within this repository and runs independently as long as the directories are defined correctly.

# About the Tool

  - **Problem/Claim Solved by the Tool:**  
    The tool calculates the reverberation time of all rooms with wooden floors, focusing on offices where most people are located. For example, a room with a volume of 193 m³ is reported to have a reverberation time of 0.63 seconds. Our script not only calculates this room quickly but also handles the remaining 42 relevant rooms. Based on the scatter plot of reverberation time vs. volume, three rooms with a volume of 193 m³ all have a reverberation time close to 0.63 seconds, verifying the claim.

  - **Source of the Problem:**  
    In the report "CES_BLD_24_0_6_MEP" (p. 22), it is stated: "With the volume of Room 1 at 193.9 m³, the reverberation time is determined to be 0.63 s."

  - **Description of the Tool:**  
    The script detects floor surfaces and surrounding surfaces to identify all rooms. It then filters out irrelevant rooms and calculates the reverberation time for the remaining relevant rooms, providing an estimate of the acoustic performance of each room.

  - **Instructions to Run the Tool:**  
    1. Open `main.py`.
    2. Ensure you have installed the required packages using the recommended `pip install` commands.
    3. In line 30, set your desired save directory to store the results.
    4. In line 92, provide the file path to your architectural IFC model.
    5. Run the script.

# Advanced Building design

  - **Relevant Design Stages (A, B, C, or D):**  
    The tool is most useful in design stages B and C, where models of the design are generated. By providing a quick overview of the acoustic performance of multiple rooms, the tool helps developers assess whether the design is acoustically efficient or if alternative designs are required.

  - **Potential Users:**  
    Engineers and architects, or anyone working on larger projects where manual calculations of reverberation times would be too time-consuming.

  - **Required Information for the Tool to Work:**  
    - A save directory and the file path to an IFC model.  
    - Surface naming conventions in the IFC model must be specified to ensure the script identifies the correct surfaces. This can be configured in step 2 of the `analyze_all_floor_arc_surfaces(ifc_model)` function.
