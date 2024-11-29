# -------------------- Script for IFC Surface Analysis and Reverberation Calculation --------------------
# This script analyzes floor surfaces in an IFC model, calculating reverberation times and visualizing results.
# Key steps include loading an IFC file, identifying relevant surfaces, and performing various geometric and acoustic calculations.

#Important - must run these commands before running the script
"""
pip install tqdm
pip install ifcopenshell
pip install numpy
pip install pandas
pip install matplotlib

"""

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

# Define the save directory
save_directory = r"C:\Users\magnu\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\Tredje semester\41934 Advanced Building Information Modeling\Vizual\Floor_Plans"

# Ensure the directory exists
os.makedirs(save_directory, exist_ok=True)

print(f"Save directory is set to: {save_directory}")



# -------------------- Load the IFC Model --------------------
# Specify the path to the IFC file (update the path if needed).
print("WELCOME")
print("THIS SCRIPT WILL LOAD AN ARCHITECTURAL IFC MODEL AND DETECT MEDIUM SIZED ROOMS SUCH AS CLASSROOMS AND OFFICES")
print("IT WILL THEN FIND: FLOOR AREA, HEIGHT, VOLUME, AVERAGE ABSORPTION AREA AND REVERBERATION TIME")
print("THIS WILL GIVE AN IDEA OF THE ACOUSTIC COMPETENCES OF EACH ROOM")
print("RECOMMENDED REVERBERATION TIME FOR CLASSROOMS IS 0.4-0.6 SECONDS WHILE LARGER ROOMS AND OFFICES CAN GO UP TO 1-1.1 SECONDS")
print("LASTLY THE VISUALISATIONS OF THE RESULTS WILL BE DISPLAYED")
print("-----------------------------------------------------------")
print("THE SCRIPT WILL TAKE A COUPLE MINUTES TO LOAD THE MODEL AND FIND APPROPRIATE ROOMS")
print("LET'S BEGIN")
# Countdown before assigning the file path
print("Starting in...")
for i in range(5, 0, -1):  # Countdown from 5 to 1
    print(f"{i} seconds remaining...")
    time.sleep(1)  # Wait for 1 second
print("Loading Architectural model...")
# Simulated Loading Bar Function

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

# Defining model path
file_path = r"C:\Users\magnu\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\Tredje semester\41934 Advanced Building Information Modeling\IFC_Models\CES_BLD_24_06_ARC.IFC"
ifc_model = load_ifc_with_progress(file_path)


# -------------------- Geometry Settings --------------------
# Set global geometry processing options for creating and analyzing 3D shapes.
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)  # Use world coordinates for all geometry.

# -------------------- Helper Functions --------------------
# The following functions perform calculations for geometry, areas, distances, and classification.
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

# -------------------- Execute Analysis and Display Results --------------------

# Run the analysis on the IFC model and display the results.
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
  

# -------------------- Visualization Section --------------------


# Check if there are results to plot
if results:
    # Extract Floor Areas and Reverberation Times
    # Extract Floor Areas, Volumes, and Reverberation Times
    floor_areas = [result['top_surface_area'] for result in results]
    volumes = [result['volume'] for result in results]  # Add this line to extract volumes
    reverberation_times = [result['reverberation_time'] for result in results]
    floor_names = [result['name'] for result in results]  # For the table

    # Assign colors based on Floor Area categories
    colors = []
    for area in floor_areas:
        if area < 50:
            colors.append('green')
        elif 50 <= area <= 100:
            colors.append('blue')
        else:
            colors.append('red')

    # Create scatter plot with smaller markers
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        floor_areas,
        reverberation_times,
        c=colors,
        alpha=0.7,
        edgecolors='w',
        s=50  # Reduced size from 100 to 50
    )

    # Create custom legend with the number of rooms
    green_patch = mpatches.Patch(color='green', label='< 50 m²')
    blue_patch = mpatches.Patch(color='blue', label='50-100 m²')
    red_patch = mpatches.Patch(color='red', label='> 100 m²')
    legend = plt.legend(
        handles=[green_patch, blue_patch, red_patch],
        title=f'Floor Area Categories\n(n={len(results)})'
    )

    # Make legend labels bold
    for text in legend.get_texts():
        text.set_fontweight('bold')

    # Compute best-fit line (linear regression)
    if len(floor_areas) > 1:
        # Fit a first-degree polynomial (linear fit)
        coefficients = np.polyfit(floor_areas, reverberation_times, 1)
        polynomial = np.poly1d(coefficients)
        # Generate x values for the fit line
        x_fit = np.linspace(min(floor_areas), max(floor_areas), 100)
        y_fit = polynomial(x_fit)
        # Plot the fit line as dotted
        plt.plot(
            x_fit,
            y_fit,
            'k--',  # 'k--' means black dashed line
            label='Best Fit Line'
        )

        # Update legend to include the fit line
        legend = plt.legend(
            handles=[green_patch, blue_patch, red_patch, plt.Line2D([], [], color='k', linestyle='--', label='Best Fit Line')],
            title=f'Floor Area Categories\n(n={len(results)})'
        )

        # Make all legend labels bold
        for text in legend.get_texts():
            text.set_fontweight('bold')

    # Set labels and title
    plt.xlabel('Floor Area (m²)', fontsize=12)
    plt.ylabel('Reverberation Time (s)', fontsize=12)
    plt.title('Reverberation Time vs. Floor Area', fontsize=14)

    # Optional: Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save and show plot
    plt.tight_layout()
    plt.show()

# -------------------- Table Section --------------------

# Create a DataFrame for better table management
df = pd.DataFrame({
    "Floor Name": floor_names,
    "Floor Area (m²)": [f"{area:.2f}" for area in floor_areas],
    "Height to Ceiling (m)": [f"{result['vertical_distance']:.2f}" for result in results],
    "Volume (m³)": [f"{result['volume']:.2f}" for result in results],
    "Wall Area (m²)": [f"{result['surrounding_areas']['Wall']:.2f}" for result in results],
    "Window Area (m²)": [f"{result['surrounding_areas']['Window']:.2f}" for result in results],
    "Beam Area (m²)": [f"{result['surrounding_areas']['Beam']:.2f}" for result in results],
    "Avg Absorption Coef.": [f"{result['avg_absorption_coefficient']:.3f}" for result in results],
    "Reverberation Time (s)": [f"{result['reverberation_time']:.3f}" if result['reverberation_time'] is not None else "N/A" for result in results]
})

# Plot the table using Pandas styling
fig, ax = plt.subplots(figsize=(14, max(2, len(df)*0.6)))  # Increased height per row
ax.axis('off')  # Hide the axes

# Create the table
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc='center',
    loc='upper center'
)

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(df.columns))))

# Increase the row height
table.scale(1, 2)  # Adjust the second parameter to control vertical spacing (default is 1)

# Apply monospaced font to all cells
for key, cell in table.get_celld().items():
    cell.set_text_props(fontfamily='monospace')

# Make column headers bold
for (i, j), cell in table.get_celld().items():
    if i == 0:
        cell.set_text_props(fontweight='bold')

plt.title('Summary of Reverberation Analysis', fontsize=14, pad=20)
plt.tight_layout()
plt.show()


 # Distribution of reverberation times
plt.figure(figsize=(8, 5))
plt.hist(reverberation_times, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(np.mean(reverberation_times), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {np.mean(reverberation_times):.2f}')
plt.axvline(np.median(reverberation_times), color='green', linestyle='dashed', linewidth=1, label=f'Median: {np.median(reverberation_times):.2f}')
plt.xlabel('Reverberation Time (s)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Reverberation Times', fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()

# Distribution of floor areas
plt.figure(figsize=(8, 5))
plt.hist(floor_areas, bins=10, color='lightgreen', edgecolor='black', alpha=0.7)
plt.axvline(np.mean(floor_areas), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {np.mean(floor_areas):.2f}')
plt.axvline(np.median(floor_areas), color='blue', linestyle='dashed', linewidth=1, label=f'Median: {np.median(floor_areas):.2f}')
plt.xlabel('Floor Area (m²)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Floor Areas', fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()

# Reverberation time vs. volume
plt.figure(figsize=(10, 6))

# Scatterplot
plt.scatter(volumes, reverberation_times, c='blue', alpha=0.7, edgecolors='w', s=50, label="Data Points")

# Compute best-fit line (linear regression)
if len(volumes) > 1:
    coefficients = np.polyfit(volumes, reverberation_times, 1)
    polynomial = np.poly1d(coefficients)
    x_fit = np.linspace(min(volumes), max(volumes), 100)
    y_fit = polynomial(x_fit)
    plt.plot(x_fit, y_fit, 'k--', label='Best Fit Line')

    # Display regression equation
    equation = f"y = {coefficients[0]:.3f}x + {coefficients[1]:.3f}"
    plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round", alpha=0.5))

# Labels and title
plt.xlabel('Volume (m³)', fontsize=12)
plt.ylabel('Reverberation Time (s)', fontsize=12)
plt.title('Reverberation Time vs. Volume', fontsize=14)

# Grid and legend
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

# Save and show the plot
plt.show()


plt.figure(figsize=(10, 6))

# Define absorption coefficients for each surface type
absorption_coefficients = {
    "Wall": 0.05,     # Absorption coefficient for painted gypsum walls.
    "Window": 0.03,   # Absorption coefficient for windows.
    "Beam": 0.05,     # Absorption coefficient for beams.
    "Ceiling": 0.6,   # Absorption coefficient for acoustic ceiling.
    "Floor": 0.07     # Absorption coefficient for wooden flooring.
}

# Prepare data for the heatmap: Absorption Area = Surface Area * Absorption Coefficient
absorption_area_data = pd.DataFrame({
    "Wall": [result['surrounding_areas']['Wall'] * absorption_coefficients["Wall"] for result in results],
    "Window": [result['surrounding_areas']['Window'] * absorption_coefficients["Window"] for result in results],
    "Beam": [result['surrounding_areas']['Beam'] * absorption_coefficients["Beam"] for result in results],
    "Ceiling": [result['surrounding_areas']['Ceiling'] * absorption_coefficients["Ceiling"] for result in results],
    "Floor": [result['surrounding_areas']['Floor'] * absorption_coefficients["Floor"] for result in results],
}).T  # Transpose for proper orientation

# Optional: Replace NaN with 0 if any
absorption_area_data = absorption_area_data.fillna(0)

# Create heatmap with matplotlib
plt.figure(figsize=(12, 6))
im = plt.imshow(absorption_area_data, cmap="YlGnBu", aspect="auto")

# Add colorbar with appropriate label
cbar = plt.colorbar(im)
cbar.set_label("Absorption Area (m² × Coefficient)", fontsize=12)

# Set x-axis labels as Room Names or Indices
plt.xticks(range(len(results)), labels=[f"Room {i+1}" for i in range(len(results))], rotation=45, ha='right')

# Set y-axis labels as Surface Types
plt.yticks(range(len(absorption_area_data.index)), labels=absorption_area_data.index)

# Add title and labels
plt.title("Absorption Areas by Surface Type and Room", fontsize=14)
plt.xlabel("Room Index", fontsize=12)
plt.ylabel("Surface Type", fontsize=12)

# Enhance layout
plt.tight_layout()

#display the heatmap
plt.show()

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatterplot in 3D
ax.scatter(floor_areas, volumes, reverberation_times, c='purple', alpha=0.7, s=50, edgecolors='w')

ax.set_xlabel('Floor Area (m²)', fontsize=12)
ax.set_ylabel('Volume (m³)', fontsize=12)
ax.set_zlabel('Reverberation Time (s)', fontsize=12)
ax.set_title('3D Scatter: Floor Area, Volume, and Reverberation Time', fontsize=14)

plt.tight_layout()
plt.show()

# Categorize rooms by size
categories = ["<50 m²", "50-100 m²", ">100 m²"]
category_times = {
    "<50 m²": [time for area, time in zip(floor_areas, reverberation_times) if area < 50],
    "50-100 m²": [time for area, time in zip(floor_areas, reverberation_times) if 50 <= area <= 100],
    ">100 m²": [time for area, time in zip(floor_areas, reverberation_times) if area > 100],
}

# Calculate average reverberation times per category
avg_times = [np.mean(category_times[cat]) if category_times[cat] else 0 for cat in categories]

# Create bar chart
plt.figure(figsize=(8, 5))
bars = plt.bar(categories, avg_times, color=['green', 'blue', 'red'], alpha=0.7)

# Set labels and title
plt.xlabel('Room Size Category', fontsize=12)
plt.ylabel('Average Reverberation Time (s)', fontsize=12)
plt.title('Average Reverberation Time by Room Size Category', fontsize=14)

# Add average value labels inside the bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # X-coordinate: center of the bar
        height / 2,                          # Y-coordinate: halfway up the bar
        f'{height:.2f}',                     # Text to display (formatted to 2 decimal places)
        ha='center',                         # Horizontal alignment
        va='center',                         # Vertical alignment
        fontsize=14,                         # Font size
        fontweight='bold',                   # Bold text
        color='white'                        # Text color for contrast
    )

# Improve layout and display the plot
plt.tight_layout()
plt.show()


# Identify outliers
threshold = 1.0  # Example threshold for reverberation time
outliers = [(area, time) for area, time in zip(floor_areas, reverberation_times) if time > threshold]

plt.figure(figsize=(10, 6))
plt.scatter(floor_areas, reverberation_times, c='blue', alpha=0.7, edgecolors='w', s=50)
for area, time in outliers:
    plt.annotate(f"Outlier ({area:.1f}, {time:.2f})", (area, time), fontsize=8, color='red')

plt.xlabel('Floor Area (m²)', fontsize=12)
plt.ylabel('Reverberation Time (s)', fontsize=12)
plt.title('Reverberation Time vs. Floor Area (Outliers Highlighted)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()