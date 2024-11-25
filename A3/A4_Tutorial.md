# IFC Surface Analysis and Reverberation Calculation Script Tutorial

Welcome! This repository contains a tutorial for using the **IFC Surface Analysis and Reverberation Calculation** script, which performs acoustic and geometric analyses on floor surfaces in an IFC model, specifically focusing on medium-sized rooms like classrooms and offices. This script also generates visualizations of the results, helping you understand the acoustic properties of the modeled spaces. Let's walk through the process step-by-step.

## Target audience
This script is intended primarily for OpenBIM Analysts Level 3, as it focuses on analyzing IFC models and evaluating room acoustics in a standalone python script. It is useful for beginners and experienced coders alike who need an efficient overview of room acoustics during the design phase.



## Complications and limitations
The current version of the script is unable to accurately analyze rooms with non-rectangular shapes. This is an area for future improvement, though the script remains highly viable for analyzing rectangular rooms, which are common in office and classroom settings. Additionally, there are some limitations in precision, meaning the results should be considered as close estimates. For situations that require precise values, further detailed calculations may be necessary. The accuracy of the script can improve with IFC models that have strict boundaries in the design phase, as the script is currently unable to fully exclude certain objects, leading to the introduction of compensating adjustments throughout the script.



## Prerequisites
Before you begin, make sure you have Python installed on your machine. The script also requires a few Python packages that need to be installed. You can do so by running the following commands in your terminal:

```sh
pip install tqdm
pip install ifcopenshell
pip install numpy
pip install pandas
pip install matplotlib
```

These packages include:
- **tqdm**: Used for creating progress bars.
- **ifcopenshell**: A library for reading and processing IFC files.
- **numpy**, **matplotlib**, and **pandas**: Libraries for data manipulation, visualization, and table management.

## Overview of the Script
The script performs the following key steps:
1. **Loads an IFC model**: Using IfcOpenShell, it reads the architectural IFC file to detect medium-sized rooms (such as classrooms and offices).
2. **Geometry Analysis**: It identifies relevant floor surfaces, bounding boxes, and other surrounding elements like walls, windows, and beams.
3. **Acoustic Analysis**: Calculates reverberation times based on surface areas, room volumes, and average absorption coefficients.
4. **Visualization**: Provides visual feedback by plotting results such as reverberation time versus floor area, 3D scatter plots, and other summary charts.

## Running the Script
### Set Up the Directory and IFC File Path
Before running the script, you need to specify the path to the IFC file and define where the generated visualizations will be saved. In the script, you will find:

```python
save_directory = r"C:\Users\Magnus\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\Tredje semester\41934 Advanced Building Information Modeling\Vizual\Floor_Plans"
file_path = r"C:\Users\Magnus\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\Tredje semester\41934 Advanced Building Information Modeling\IFC_Models\CES_BLD_24_06_ARC.IFC"
```

Update these paths based on where your IFC files and save directory are located on your system.

### Start the Analysis
When you run the script, it begins by printing a welcome message explaining what it will do. It will then count down for a few seconds before starting the analysis, giving you a moment to make sure everything is ready.

```python
print("WELCOME")
print("THIS SCRIPT WILL LOAD AN ARCHITECTURAL IFC MODEL AND DETECT MEDIUM SIZED ROOMS SUCH AS CLASSROOMS AND OFFICES")
# Countdown before assigning the file path
print("Starting in...")
for i in range(5, 0, -1):
    print(f"{i} seconds remaining...")
    time.sleep(1)  # Wait for 1 second
print("Loading Architectural model...")
```

### Load the IFC Model
The script provides a loading progress bar as it reads and processes the IFC model using IfcOpenShell. This ensures you know how far along the loading process is.

```python
def load_ifc_with_progress(file_path):
    with tqdm(total=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}%", colour="green") as pbar:
        # Model loading simulation and actual loading
        ifc_model = ifcopenshell.open(file_path)
        pbar.update(100)
    return ifc_model
```

### Analyze Geometry and Acoustic Properties
The script then analyzes the geometry of the building, focusing on medium-sized floor slabs that meet the criteria of being suitable for classrooms or offices.
- It filters out rooms that are too large or too small, or those that are not rectangular. The filters for this script has been chosen this way to target specifically classrooms and offices for the analysis as this is where most people will be located with acoustic needs.
- It calculates the floor area, height, volume, and surrounding surface types (e.g., walls, beams, windows).
- The script uses these details to estimate reverberation times based on Sabine's formula.

### Display and Visualize Results
Once all rooms are analyzed, the results are printed in the console. They include:
- Floor Area
- Height to Ceiling
- Volume
- Average Absorption Coefficient
- Reverberation Time

The script also creates several visualizations using **matplotlib**, such as:
- **Scatter plots**: To visualize relationships between floor area and reverberation time.
- **Histograms**: To show the distribution of reverberation times and floor areas.
- **3D Plots**: To show relationships between floor area, volume, and reverberation time.

Here's an example of how a scatter plot is generated:

```python
plt.scatter(floor_areas, reverberation_times, c=colors, alpha=0.7, edgecolors='w', s=50)
plt.xlabel('Floor Area (m²)', fontsize=12)
plt.ylabel('Reverberation Time (s)', fontsize=12)
plt.title('Reverberation Time vs. Floor Area', fontsize=14)
plt.show()
```

## Key Functions Explained

### Helper Functions
The script uses several helper functions to make the analysis easier:
- **`get_top_surface_area(surface)`**: Calculates the area of the top-facing surface of the floor slab.
- **`is_rectangular(surface, tolerance=0.05)`**: Checks if a given surface is rectangular within a tolerance level of 5%, which is important for considering only standard-shaped rooms.
- **`calculate_reverberation_time(volume, avg_absorption_coefficient, total_surface_area)`**: Uses Sabine's formula to estimate reverberation time based on room characteristics.

### Analysis Function
- **`analyze_all_floor_arc_surfaces(ifc_model)`**: This is the main analysis function, which iterates through all floor surfaces in the IFC model, calculates the desired metrics, and then appends the results for each eligible surface to a results list.

## Tips for Effective Usage
1. **Adjust the Surface Filtering Criteria**: Depending on your use case, you might need to adjust the filtering criteria for room sizes. This can be done in the `analyze_all_floor_arc_surfaces` function.
2. **Check IFC Model Quality**: Ensure that your IFC model has correctly defined surfaces and that the attributes used in filtering are properly assigned. The script relies on surface names and types, so incorrect or incomplete data could lead to missed surfaces.
3. **Customize Visualization**: You can add or remove visualizations based on your needs. If you want more specific visual feedback, feel free to modify the plotting sections.

## Extending the Script
- **Adding More Room Types**: Currently, the script looks for "Floor:ARC - Wood flooring". You can modify it to analyze other room types by changing the filtering criteria.
- **Advanced Acoustic Modeling**: For more precise acoustic analysis, consider integrating more detailed absorption coefficients based on material properties.
- **Exporting Results**: If you need to export the results to a CSV or Excel file, you can easily extend the script using the `pandas` library to write the `results` DataFrame to a file:

  ```python
  df.to_csv("reverberation_analysis_results.csv", index=False)
  ```

## Conclusion
This script is a strong tool for performing acoustic analysis of IFC models, giving you insights into the reverberation characteristics of various rooms. Remember that calculations are estimates close to the correct value and not precise. With customization, you can adapt it for a wide range of building types and specific analyses. The provided visualizations help in better understanding the spatial and acoustic properties of your architectural model. Feel free to adjust and extend the script as needed for your projects.

