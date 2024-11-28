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
This will give a brief overview of what the script does and at the end of the tutorial all parts of the script will be displayed and explained thoroughly. The script performs the following key steps:
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


















# Detailed explanation the script
## Loading phase

### Importing libraries and defining save directory
```
import ifcopenshell
import ifcopenshell.geom
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches  # For legend patches
import pandas as pd  # To create and manage data tables
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
import time
from tqdm import tqdm
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon

#Define the save directory
save_directory = r"C:\Users\Magnus\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\Tredje semester\41934 Advanced Building Information Modeling\Vizual\Floor_Plans"

#Ensure the directory exists
os.makedirs(save_directory, exist_ok=True)

print(f"Save directory is set to: {save_directory}")
```


```
def load_ifc_with_progress(file_path):
    """
    Simulate a progress bar during IFC file loading and related tasks.

    Parameters:
    - file_path (str): Path to the IFC file.

    Returns:
    - ifc_model: The loaded IFC model.
    """
    total_steps = 100
    progress = 0
    with tqdm(total=total_steps, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}%", colour="green") as pbar:
        # Simulate pre-loading (cosmetic only)
        for _ in range(30):
            time.sleep(0.05)  # Fast cosmetic delay
            pbar.update(1)
            progress += 1

        # Actual model loading (real time)
        ifc_model = ifcopenshell.open(file_path)
        pbar.update(50)  # Simulate jumping to 80% after loading
        progress += 50

        # Simulate post-loading tasks (e.g., processing geometry)
        for _ in range(20):
            time.sleep(0.05)  # Fast cosmetic delay
            pbar.update(1)
            progress += 1

    print("Model successfully loaded and ready for analysis!")
    return ifc_model

# Example Usage
file_path = r"C:\Users\Magnus\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\Tredje semester\41934 Advanced Building Information Modeling\IFC_Models\CES_BLD_24_06_ARC.IFC"
ifc_model = load_ifc_with_progress(file_path)
```


## Calculation and analyzing

### Reduction Factor function
The functions adjusts the surface area when detecting a 352mm thick external wall. The script has not been able to only pick the surface facing the room, but it calculates the whole surface area of the object and this factor reduces the surface are to the right face.
```
def reduction_factor(a, b, t=352):
    """
    Calculate the reduction factor for a rectangular shape. 

    Reason:
    The surface area is only found as the whole surface of an object. The reduction factor is specifically for this model
    where external walls have a thickness of 352mm. To extract only the area of the internal side of these walls a reduction
    factor has been found and it is dependent on the lenght and height of the wall piece and the thickness.

    Parameters:
    - a (float): Length of one side of the rectangle.
    - b (float): Length of the other side of the rectangle.
    - t (float): Thickness of the material (default is 352).

    Returns:
    - float: Reduction factor.
    """
    return (a * b) / (2 * (a * b) + 2 * (b * t) + 2 * (a * t))
```


### Face area function
This functions calculates the surface area of the face facing the room from an external wall object with a thickness of 352mm.
```
def face_area(a, b, t=352, total_area=None):
    """
    Calculate the reduced area of a face using the reduction factor.

    Returns:
    - float: Adjusted face area.
    """
    if total_area is None:
        total_area = 2 * (a * b) + 2 * (b * t) + 2 * (a * t)
    R = reduction_factor(a, b, t)
    return R * total_area
```


### Top surface are

```
def get_top_surface_area(surface):
    """
    Calculate the area of upward-facing (top) surfaces.

    Parameters:
    - surface: IFC surface object to analyze.

    Returns:
    - float: Total area of upward-facing surfaces.
    """
    try:
        shape = ifcopenshell.geom.create_shape(settings, surface)
        verts = shape.geometry.verts  # List of vertex coordinates.
        faces = shape.geometry.faces  # Indices of vertices forming faces.

        vertices = np.array(verts).reshape(-1, 3)  # Reshape vertices into [x, y, z] format.
        total_area = 0  # Initialize total area.

        for i in range(0, len(faces), 3):
            # Extract vertex indices for the triangle face.
            idx1, idx2, idx3 = faces[i], faces[i + 1], faces[i + 2]
            v1, v2, v3 = vertices[idx1], vertices[idx2], vertices[idx3]

            # Calculate the normal vector of the triangle.
            normal = np.cross(v2 - v1, v3 - v1)
            normal_length = np.linalg.norm(normal)
            if normal_length == 0:
                continue  # Skip degenerate triangles.
            normal_unit = normal / normal_length

            # Check if the face is facing upwards.
            if normal_unit[2] > 0.9:  # Adjust threshold for upward orientation.
                area = normal_length / 2  # Triangle area formula.
                total_area += area

        return total_area
    except Exception as e:
        return 0  # Return 0 if an error occurs.
```

### Bounding box function

```
def get_bounding_box(surface):
    """
    Compute the bounding box (the smallest 3D rectangular box that contains the object) of a surface.

    Parameters:
    - surface: The IFC surface object for which the bounding box is calculated.

    Returns:
    - tuple: (min_coords, max_coords), where:
        - min_coords: A numpy array of the smallest [x, y, z] coordinates of the bounding box.
        - max_coords: A numpy array of the largest [x, y, z] coordinates of the bounding box.
    - If an error occurs (e.g., invalid surface), returns (None, None).
    """
    try:
        shape = ifcopenshell.geom.create_shape(settings, surface)  # Generate 3D geometry for the surface.
        verts = shape.geometry.verts  # List of vertex coordinates (flattened).
        vertices = np.array(verts).reshape(-1, 3)  # Reshape into a list of [x, y, z] points.

        min_coords = np.min(vertices, axis=0)  # Find the smallest [x, y, z] values.
        max_coords = np.max(vertices, axis=0)  # Find the largest [x, y, z] values.

        return min_coords, max_coords  # Return the bounding box coordinates.
    except Exception as e:
        return None, None  # Return None if there's an error.
```

### Sample points function

```
def get_sample_points(surface):
    """
    Get the center point of a surface. The center point is calculated as the midpoint of the bounding box.

    Parameters:
    - surface: The IFC surface object to analyze.

    Returns:
    - list: A list containing one numpy array representing the center point [x, y, z].
        - The Z-coordinate is set to the top (maximum) Z value of the bounding box.
    - If the bounding box cannot be calculated, returns an empty list.
    """
    min_coords, max_coords = get_bounding_box(surface)  # Get bounding box limits.
    if min_coords is None or max_coords is None:
        return []  # Return an empty list if the bounding box is invalid.

    center = (min_coords + max_coords) / 2  # Compute the midpoint.
    center[2] = max_coords[2]  # Set Z to the top surface level.

    return [center]  # Return the center point as a list.
```

### Function to measure vertical height of room
```
def measure_vertical_distances_to_ifccovering(surface, coverings):
    """
    Measure vertical distances from a surface to the closest coverings (e.g., ceilings).

    Parameters:
    - surface: The IFC surface object for which distances are calculated.
    - coverings: A list of covering objects, each with pre-calculated bounding boxes (min_coords, max_coords).

    Returns:
    - list: A list of vertical distances (float) from the surface's sample points to the nearest coverings.
        - If no covering is above a point, the distance is set to None.
    """
    points = get_sample_points(surface)  # Get center point of the surface.
    if not points:
        return []  # Return an empty list if there are no valid sample points.

    distances = []  # Initialize list to store distances.
    for point in points:
        closest_distance = float('inf')  # Initialize closest distance to a very large number.
        point_xy = point[:2]  # Use only the X and Y coordinates for horizontal alignment.

        # Check each covering for alignment and distance.
        for covering in coverings:
            min_coords = covering['min_coords']
            max_coords = covering['max_coords']

            # Check if the point is within the horizontal bounds of the covering.
            if (min_coords[0] <= point_xy[0] <= max_coords[0] and
                min_coords[1] <= point_xy[1] <= max_coords[1]):
                # Check if the covering is above the point.
                if min_coords[2] >= point[2]:
                    distance = min_coords[2] - point[2]  # Calculate vertical distance.
                    if distance < closest_distance:
                        closest_distance = distance  # Update the closest distance.

        distances.append(closest_distance if closest_distance != float('inf') else None)

    return distances  # Return the list of distances.
```



### Filter-function to check if rectangular
```
def is_rectangular(surface, tolerance=0.05):
    """
    Determine if a surface is rectangular by comparing the top surface area to its bounding box area.

    Parameters:
    - surface: The IFC surface object to analyze.
    - tolerance (float): Allowed deviation ratio for considering the surface as rectangular (default is 5%).

    Returns:
    - bool: True if the surface is rectangular within the given tolerance, False otherwise.
    """
    min_coords, max_coords = get_bounding_box(surface)  # Get bounding box limits.
    if min_coords is None or max_coords is None:
        return False  # Return False if the bounding box is invalid.

    # Calculate dimensions of the bounding box.
    bbox_length = max_coords[0] - min_coords[0]  # Length along the X-axis.
    bbox_width = max_coords[1] - min_coords[1]   # Width along the Y-axis.
    bbox_area = bbox_length * bbox_width  # Compute the bounding box area.

    # Calculate the top surface area of the surface.
    top_surface_area = get_top_surface_area(surface)

    if bbox_area == 0:
        return False  # Return False if the bounding box area is zero.

    # Calculate the ratio of the top surface area to the bounding box area.
    ratio = top_surface_area / bbox_area

    # Check if the ratio is within the acceptable tolerance.
    return abs(ratio - 1.0) <= tolerance
```

### Surrounding surfaces function
```
def classify_surrounding_surfaces(surface, vertical_distance, nearby_elements):
    """
    Classify and calculate areas of surrounding surfaces (walls, windows, beams) relative to a given floor surface.

    This function identifies and processes elements like walls, windows, and beams that are near the given floor surface.
    It calculates the area of their relevant faces and classifies the surfaces by their type (Wall, Window, Beam).

    Parameters:
    - surface: The IFC surface object (floor) being analyzed.
    - vertical_distance (float): The vertical distance from the floor to the ceiling.
    - nearby_elements (list): A list of elements near the surface, where each element is a dictionary containing:
        - 'element': The IFC object.
        - 'type': The type of element (Wall, Window, Beam).
        - 'min_coords': Minimum bounding box coordinates of the element.
        - 'max_coords': Maximum bounding box coordinates of the element.

    Returns:
    - dict: A dictionary with total classified areas for each surface type:
        {"Wall": area, "Window": area, "Beam": area}.
    """
    # Initialize the area totals for each surface type.
    surrounding_areas = {"Wall": 0, "Window": 0, "Beam": 0}

    # Get the bounding box of the given surface (floor).
    min_coords, max_coords = get_bounding_box(surface)
    if min_coords is None or max_coords is None:
        return surrounding_areas  # Return default if the bounding box is invalid.

    # Define the vertical range (floor to ceiling) and top Z-coordinate of the surface.
    floor_z = min_coords[2]
    ceiling_z = floor_z + vertical_distance
    surface_top_z = max_coords[2]

    # Add a small margin around the floor area to include nearby elements.
    margin = 0.5  # 0.5 meters.
    min_x = min_coords[0] - margin
    max_x = max_coords[0] + margin
    min_y = min_coords[1] - margin
    max_y = max_coords[1] + margin

    # Process each nearby element to determine its classification and calculate its area.
    for elem in nearby_elements:
        obj = elem['element']  # The IFC object.
        obj_name = obj.Name or ""  # Object name (may be empty).
        element_type = elem['type']  # Type of the element (Wall, Window, Beam).
        obj_min_coords = elem['min_coords']  # Bounding box minimum coordinates.
        obj_max_coords = elem['max_coords']  # Bounding box maximum coordinates.

        try:
            # Retrieve or create the shape geometry of the element.
            if 'shape' in elem:
                shape = elem['shape']  # Use cached shape if available.
            else:
                shape = ifcopenshell.geom.create_shape(settings, obj)
                elem['shape'] = shape  # Cache the shape for future use.

            # Extract vertices and faces from the shape geometry.
            verts = shape.geometry.verts  # List of vertex coordinates.
            faces = shape.geometry.faces  # Indices defining faces.
            vertices = np.array(verts).reshape(-1, 3)  # Reshape into [x, y, z] format.

            # Iterate through the faces of the shape.
            for i in range(0, len(faces), 3):
                # Get vertex indices for the current face.
                idx1, idx2, idx3 = faces[i], faces[i + 1], faces[i + 2]
                v1, v2, v3 = vertices[idx1], vertices[idx2], vertices[idx3]

                # Calculate the normal vector for the face.
                normal = np.cross(v2 - v1, v3 - v1)
                normal_length = np.linalg.norm(normal)
                if normal_length == 0:
                    continue  # Skip degenerate faces.
                normal_unit = normal / normal_length  # Normalize the normal vector.

                # Check if the face is approximately vertical.
                if abs(normal_unit[2]) < 0.1:  # Small Z-component indicates vertical orientation.
                    # Calculate the center of the face.
                    face_center = (v1 + v2 + v3) / 3
                    face_x, face_y, face_z = face_center

                    # Check if the face is within the vertical range (top of surface to ceiling).
                    if surface_top_z <= face_z <= ceiling_z:
                        # Check if the face is within the horizontal bounds (with margin).
                        if min_x <= face_x <= max_x and min_y <= face_y <= max_y:
                            # Calculate the face area (triangle area formula).
                            area = normal_length / 2

                            # Classify the face based on the element type and adjust its area.
                            if element_type == "Wall":
                                if "Ect. Wall - 352mm" in obj_name:
                                    # Calculate reduced area for specific wall types.
                                    a = obj_max_coords[0] - obj_min_coords[0]  # Length along X-axis.
                                    b = obj_max_coords[2] - obj_min_coords[2]  # Height along Z-axis.
                                    reduced_area = face_area(a, b, t=352, total_area=area)
                                    surrounding_areas[element_type] += reduced_area
                                else:
                                    # Reduce area by 50% for other walls.
                                    surrounding_areas[element_type] += area * 0.5
                            elif element_type == "Window":
                                # Reduce area by 50% for windows.
                                surrounding_areas[element_type] += area * 0.5
                            elif element_type == "Beam":
                                # Approximation: reduce area by 80% for beams.
                                surrounding_areas[element_type] += area * 0.2
        except Exception as e:
            continue  # Skip elements if any error occurs during processing.

    return surrounding_areas  # Return the classified areas for walls, windows, and beams.
```
### Absorption coefficient calculation function
```
def calculate_absorption_coefficients(surrounding_areas, top_surface_area):
    """
    Calculate absorption coefficients and percentages for surrounding surfaces.

    Parameters:
    - surrounding_areas (dict): A dictionary containing surface types (Wall, Window, Beam, Floor, Ceiling) as keys 
                                and their respective areas as values.
    - top_surface_area (float): The area of the floor (and ceiling).

    Returns:
    - tuple: (absorption_percentages, avg_absorption_coefficient)
        - absorption_percentages (dict): Percentage of each surface type's area relative to the total area.
        - avg_absorption_coefficient (float): Weighted average absorption coefficient based on surface areas.
    """
    # Define absorption coefficients for each surface type.
    coefficients = {
        "Wall": 0.05,   # Absorption coefficient for painted gypsum walls.
        "Window": 0.03, # Absorption coefficient for windows.
        "Beam": 0.05,   # Absorption coefficient for beams.
        "Floor": 0.07,  # Absorption coefficient for wooden flooring.
        "Ceiling": 0.6  # Absorption coefficient for acoustic ceiling.
    }

    # Calculate the total area of all surfaces including floor and ceiling.
    total_area = sum(surrounding_areas.values())
    if total_area == 0:
        return {}, 0  # Return empty results if no area is present.

    # Initialize variables for absorption calculations.
    absorption_sum = 0
    absorption_percentages = {}

    # Calculate percentages and absorption contributions for each surface type.
    for surface_type, area in surrounding_areas.items():
        percentage = (area / total_area) * 100  # Calculate percentage contribution of the surface.
        absorption_percentages[surface_type] = percentage
        absorption_sum += coefficients.get(surface_type, 0) * area  # Add weighted absorption contribution.

    # Calculate the average absorption coefficient.
    avg_absorption_coefficient = absorption_sum / total_area
    return absorption_percentages, avg_absorption_coefficient
```

### Reverberation time function
```
def calculate_reverberation_time(volume, avg_absorption_coefficient, total_surface_area):
    """
    Calculate the reverberation time using Sabine's formula.

    Parameters:
    - volume (float): Volume of the room (m³).
    - avg_absorption_coefficient (float): Average absorption coefficient of the room's surfaces.
    - total_surface_area (float): Total surface area of the room (m²).

    Returns:
    - float or None: Reverberation time (seconds), or None if the absorption coefficient is zero.
    """
    if avg_absorption_coefficient == 0:
        return None  # Reverberation time cannot be calculated without absorption.
    return 0.161 * volume / (total_surface_area * avg_absorption_coefficient)  # Sabine's formula.

```

### Function to analyze floors
```
def analyze_all_floor_arc_surfaces(ifc_model):
    """
    Analyze all 'Floor:ARC' surfaces in the IFC model to calculate reverberation-related metrics.

    Parameters:
    - ifc_model: The loaded IFC model object.

    Returns:
    - list: A list of dictionaries containing analysis results for each eligible floor surface.
    """
    results = []  # List to store results for each floor.

    # Step 1: Pre-process coverings (e.g., ceilings) and extract their bounding boxes.
    coverings = []
    for covering in ifc_model.by_type('IfcCovering'):
        min_coords, max_coords = get_bounding_box(covering)
        if min_coords is None or max_coords is None:
            continue  # Skip coverings without valid bounding boxes.
        coverings.append({'element': covering, 'min_coords': min_coords, 'max_coords': max_coords})

    # Step 2: Pre-process other elements (walls, windows, beams) for later classification.
    elements = []
    for obj in ifc_model.by_type('IfcProduct'):
        obj_name = obj.Name or ""  # Get the object's name.
        # Determine the element type based on its name.
        if "Interior wall - Wood" in obj_name or "Ext. Wall" in obj_name or "Ect. Wall - 352mm" in obj_name:
            element_type = "Wall"
        elif any(keyword in obj_name for keyword in ["Panel", "Glazed", "glass"]):
            element_type = "Window"
        elif "IfcMember" in obj_name or "Mullion" in obj_name:
            element_type = "Beam"
        else:
            continue  # Skip elements that don't match any category.

        # Extract bounding box for the element.
        obj_min_coords, obj_max_coords = get_bounding_box(obj)
        if obj_min_coords is None or obj_max_coords is None:
            continue

        elements.append({
            'element': obj,
            'min_coords': obj_min_coords,
            'max_coords': obj_max_coords,
            'type': element_type
        })

    # Step 3: Process each floor surface in the model.
    print("Filtering rooms...")
    for surface in ifc_model.by_type("IfcSlab"):
        if "Floor:ARC - Wood flooring" in (surface.Name or ""):
            # Calculate the top surface area of the floor.
            top_surface_area = get_top_surface_area(surface)
            if top_surface_area < 15:
                print(f"{surface.Name} filtered out due to area below 15 m² (Actual area: {top_surface_area:.2f} m²).")
                continue
            if top_surface_area > 150:
                print(f"{surface.Name} filtered out due to exceeding area limit of 150 m² (Actual area: {top_surface_area:.2f} m²).")
                continue

            # Check if the floor surface is rectangular.
            if not is_rectangular(surface, tolerance=0.05):  # Allowable tolerance: 5%.
                print(f"{surface.Name} filtered out because it is not rectangular.")
                continue

            # Get the bounding box of the floor surface.
            floor_min_coords, floor_max_coords = get_bounding_box(surface)
            if floor_min_coords is None or floor_max_coords is None:
                continue

            # Step 4: Measure vertical distances to the nearest ceiling.
            filtered_coverings = []
            for covering in coverings:
                min_c = covering['min_coords']
                max_c = covering['max_coords']
                # Check if the covering is horizontally aligned with the floor.
                if (max_c[0] >= floor_min_coords[0] and min_c[0] <= floor_max_coords[0] and
                    max_c[1] >= floor_min_coords[1] and min_c[1] <= floor_max_coords[1]):
                    filtered_coverings.append(covering)

            distances = measure_vertical_distances_to_ifccovering(surface, filtered_coverings)
            if any(distance is not None and distance > 3.1 for distance in distances):
                actual_distance = max([d for d in distances if d is not None], default=0)
                print(f"{surface.Name} filtered out due to exceeding ceiling distance (Actual height: {actual_distance:.2f} m).")
                continue

            valid_distances = [d for d in distances if d is not None]
            if not valid_distances:
                print(f"Cannot proceed without a valid ceiling height for {surface.Name}.")
                continue
            vertical_distance = sum(valid_distances) / len(valid_distances)

            # Step 5: Classify surrounding surfaces and calculate areas.
            margin = 0.5  # Extend analysis area by 0.5 meters around the floor.
            min_x = floor_min_coords[0] - margin
            max_x = floor_max_coords[0] + margin
            min_y = floor_min_coords[1] - margin
            max_y = floor_max_coords[1] + margin

            # Filter elements within the analysis area.
            nearby_elements = []
            for elem in elements:
                elem_min_coords = elem['min_coords']
                elem_max_coords = elem['max_coords']
                if (elem_max_coords[0] >= min_x and elem_min_coords[0] <= max_x and
                    elem_max_coords[1] >= min_y and elem_min_coords[1] <= max_y):
                    nearby_elements.append(elem)

            surrounding_areas = classify_surrounding_surfaces(surface, vertical_distance, nearby_elements)

            # Step 6: Calculate room properties.
            volume = top_surface_area * vertical_distance  # Room volume.

            # Add floor and ceiling areas to surrounding_areas for the absorption calculation.
            surrounding_areas['Floor'] = top_surface_area  # Area of the floor.
            surrounding_areas['Ceiling'] = top_surface_area  # Area of the ceiling.

            # Calculate absorption percentages and coefficients.
            absorption_percentages, avg_absorption_coefficient = calculate_absorption_coefficients(surrounding_areas, top_surface_area)

            # Update total surface area by including all surrounding surfaces, ceiling, and floor areas.
            total_surface_area = sum(surrounding_areas.values())

            # Step 7: Calculate reverberation time.
            rt = calculate_reverberation_time(volume, avg_absorption_coefficient, total_surface_area)


            # Append results for this floor.
            results.append({
                "name": surface.Name,
                "top_surface_area": top_surface_area,
                "vertical_distance": vertical_distance,
                "volume": volume,
                "absorption_percentages": absorption_percentages,
                "surrounding_areas": surrounding_areas,
                "avg_absorption_coefficient": avg_absorption_coefficient,
                "reverberation_time": rt
            })

    return results  # Return analysis results for all eligible floors.
```




### Running the analysis

```
results = analyze_all_floor_arc_surfaces(ifc_model)
print("\nFinal Results:")
for result in results:
    print(f"  {result['name']}:")
    print(f"    Floor Area: {result['top_surface_area']:.2f} m²")
    print(f"    Height to Ceiling: {result['vertical_distance']:.2f} m")
    print(f"    Volume: {result['volume']:.2f} m³")
    absorption_details = ', '.join([
        f"{k}: {v:.2f}% ({result['surrounding_areas'][k]:.2f} m²)" 
        for k, v in result['absorption_percentages'].items()
    ])
    print(f"    Absorption Percentages: {absorption_details}")
    print(f"    Average Absorption Coefficient: {result['avg_absorption_coefficient']:.3f}")
    if result['reverberation_time'] is not None:
        print(f"    Reverberation Time: {result['reverberation_time']:.3f} s")
    else:
        print(f"    Reverberation Time: Cannot be calculated (average absorption coefficient is zero)")
```

##

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

```

