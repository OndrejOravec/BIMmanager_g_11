import ifcopenshell
import ifcopenshell.geom
import math
import os
import numpy as np

# Load the IFC model
file_path = r"C:\Users\Magnus\OneDrive - Danmarks Tekniske Universitet\DTU\Kandidat\Tredje semester\41934 Advanced Building Information Modeling\IFC_Models\CES_BLD_24_06_ARC.IFC"
ifc_model = ifcopenshell.open(file_path)

def get_top_surface_area(surface):
    """Calculate the area of upward-facing surfaces (top surface) of a given IfcSurface."""
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    try:
        shape = ifcopenshell.geom.create_shape(settings, surface)
        verts = shape.geometry.verts  # Flat list of coordinates
        faces = shape.geometry.faces  # Indices into the verts list

        # Reshape the verts list into a list of [x, y, z] coordinates
        vertices = np.array(verts).reshape(-1, 3)

        total_area = 0
        for i in range(0, len(faces), 3):
            idx1 = faces[i]
            idx2 = faces[i + 1]
            idx3 = faces[i + 2]

            v1 = vertices[idx1]
            v2 = vertices[idx2]
            v3 = vertices[idx3]

            # Calculate the normal vector of the triangle
            normal = np.cross(v2 - v1, v3 - v1)
            normal_length = np.linalg.norm(normal)
            if normal_length == 0:
                continue  # Degenerate triangle
            normal_unit = normal / normal_length

            # Check if the face is upward-facing
            if normal_unit[2] > 0.9:  # Adjust threshold as needed
                # Calculate area of the triangle
                area = normal_length / 2
                total_area += area

        return total_area
    except Exception as e:
        print(f"Error calculating surface area for {surface.Name}: {e}")
        return 0

def get_bounding_box(surface):
    """Compute the bounding box of the surface from its geometry."""
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    try:
        shape = ifcopenshell.geom.create_shape(settings, surface)
        verts = shape.geometry.verts  # Flat list of coordinates
        vertices = np.array(verts).reshape(-1, 3)

        min_coords = np.min(vertices, axis=0)
        max_coords = np.max(vertices, axis=0)

        return min_coords, max_coords
    except Exception as e:
        print(f"Error calculating bounding box for {surface.Name}: {e}")
        return None, None

def get_sample_points(surface):
    """Get the 5 sample points (center and near corners) of a surface."""
    min_coords, max_coords = get_bounding_box(surface)
    if min_coords is None or max_coords is None:
        return []

    # Offset from edges for corner points
    offset = 0.2  # 20 cm

    # Calculate the center and 4 corner points
    center = (min_coords + max_coords) / 2
    corner1 = min_coords + [offset, offset, 0]
    corner2 = [max_coords[0] - offset, min_coords[1] + offset, min_coords[2]]
    corner3 = max_coords - [offset, offset, 0]
    corner4 = [min_coords[0] + offset, max_coords[1] - offset, min_coords[2]]

    # The Z-coordinate should be at the top surface level
    top_z = max_coords[2]

    center[2] = top_z
    corner1[2] = top_z
    corner2[2] = top_z
    corner3[2] = top_z
    corner4[2] = top_z

    return [center, corner1, corner2, corner3, corner4]

def measure_vertical_distances_to_ifccovering(surface, ifc_model):
    """Measure vertical distances to the closest IfcCovering (ceiling) for each point."""
    points = get_sample_points(surface)
    if not points:
        return []

    distances = []
    for point in points:
        closest_distance = float('inf')
        point_xy = point[:2]  # Ignore Z for horizontal alignment

        # Iterate over all IfcCovering elements to find the closest one above
        for obj in ifc_model.by_type("IfcCovering"):
            min_coords, max_coords = get_bounding_box(obj)
            if min_coords is None or max_coords is None:
                continue

            # Check horizontal alignment
            if (min_coords[0] <= point_xy[0] <= max_coords[0] and
                min_coords[1] <= point_xy[1] <= max_coords[1]):
                # Check if covering is above the point
                if min_coords[2] >= point[2]:  # Changed '>' to '>=' for exact matches
                    distance = min_coords[2] - point[2]
                    if distance < closest_distance:
                        closest_distance = distance

        if closest_distance != float('inf'):
            distances.append(closest_distance)
        else:
            distances.append(None)

    # Debug: Print the calculated distances
    print(f"  Sample points vertical distances: {distances}")
    return distances

def classify_surrounding_surfaces(surface, vertical_distance, ifc_model):
    """Classify surrounding surfaces (wall, window, door, beam) based on object names and face orientations."""
    surrounding_areas = {"Wall": 0, "Window": 0, "Door": 0, "Beam": 0}
    min_coords, max_coords = get_bounding_box(surface)
    if min_coords is None or max_coords is None:
        return surrounding_areas

    floor_z = min_coords[2]
    ceiling_z = floor_z + vertical_distance
    surface_top_z = max_coords[2]

    # Define a margin around the floor area
    margin = 0.5  # 0.5 meters
    min_x = min_coords[0] - margin
    max_x = max_coords[0] + margin
    min_y = min_coords[1] - margin
    max_y = max_coords[1] + margin

    # Elements to consider (all products in the IFC model)
    elements = ifc_model.by_type('IfcProduct')

    for obj in elements:
        obj_name = obj.Name or ""

        # Determine the element type based on name
        if "Interior wall - Wood" in obj_name or "Ext. Wall" in obj_name:
            element_type = "Wall"
        elif any(keyword in obj_name for keyword in ["Panel", "Glazed", "glass"]):
            element_type = "Window"
        elif "IfcDoor" in obj_name or "Door" in obj_name:
            element_type = "Door"
        elif "IfcMember" in obj_name or "Mullion" in obj_name:
            element_type = "Beam"
        else:
            continue  # Skip elements that don't match any category

        obj_min_coords, obj_max_coords = get_bounding_box(obj)
        if obj_min_coords is None or obj_max_coords is None:
            continue

        # Check if the object is within the horizontal bounds
        if (obj_max_coords[0] >= min_x and obj_min_coords[0] <= max_x and
            obj_max_coords[1] >= min_y and obj_min_coords[1] <= max_y):
            # Process the object's geometry
            settings = ifcopenshell.geom.settings()
            settings.set(settings.USE_WORLD_COORDS, True)
            try:
                shape = ifcopenshell.geom.create_shape(settings, obj)
                verts = shape.geometry.verts
                faces = shape.geometry.faces
                vertices = np.array(verts).reshape(-1, 3)
                for i in range(0, len(faces), 3):
                    idx1 = faces[i]
                    idx2 = faces[i + 1]
                    idx3 = faces[i + 2]
                    v1 = vertices[idx1]
                    v2 = vertices[idx2]
                    v3 = vertices[idx3]

                    # Compute face normal
                    normal = np.cross(v2 - v1, v3 - v1)
                    normal_length = np.linalg.norm(normal)
                    if normal_length == 0:
                        continue  # Skip degenerate face
                    normal_unit = normal / normal_length

                    # Check if face is vertical
                    if abs(normal_unit[2]) < 0.1:
                        # Compute face center
                        face_center = (v1 + v2 + v3) / 3
                        face_x, face_y, face_z = face_center

                        # Check if face is within vertical bounds
                        if surface_top_z <= face_z <= ceiling_z:
                            # Check if face is within horizontal bounds
                            if min_x <= face_x <= max_x and min_y <= face_y <= max_y:
                                # Calculate face area
                                area = normal_length / 2
                                if element_type == "Beam":
                                    area *= 0.2  # Approximation for beams
                                surrounding_areas[element_type] += area
            except Exception as e:
                print(f"Error processing geometry for {obj_name}: {e}")
                continue

    # Debug: Print the classified areas
    print(f"  Classified surrounding areas: {surrounding_areas}")
    return surrounding_areas



def calculate_absorption_coefficients(surrounding_areas):
    """Calculate the absorption coefficients based on surface areas."""
    coefficients = {
        "Wall": 0.2,
        "Window": 0.1,
        "Door": 0.3,
        "Beam": 0.05
    }

    total_area = sum(surrounding_areas.values())
    if total_area == 0:
        return {}, 0

    absorption_sum = 0
    absorption_percentages = {}
    for surface_type, area in surrounding_areas.items():
        percentage = (area / total_area) * 100
        absorption_percentages[surface_type] = percentage
        absorption_sum += coefficients.get(surface_type, 0) * area

    avg_absorption_coefficient = absorption_sum / total_area
    return absorption_percentages, avg_absorption_coefficient

def calculate_reverberation_time(volume, avg_absorption_coefficient, total_surface_area):
    """Calculate the reverberation time using Sabine's formula."""
    if avg_absorption_coefficient == 0:
        return None
    return 0.161 * volume / (total_surface_area * avg_absorption_coefficient)

def analyze_all_floor_arc_surfaces(ifc_model):
    """Analyze all 'Floor:ARC' surfaces."""
    results = []

    for surface in ifc_model.by_type("IfcSlab"):
        if "Floor:ARC - Wood flooring" in (surface.Name or ""):
            print(f"Analyzing {surface.Name}...")

            # Calculate top surface area (upward-facing surfaces)
            top_surface_area = get_top_surface_area(surface)
            print(f"  Calculated top surface area: {top_surface_area:.2f} m²")
            if top_surface_area < 30:
                print(f"  {surface.Name} filtered out due to area below 30 m².")
                continue

            # Measure vertical distances to the closest ceiling
            distances = measure_vertical_distances_to_ifccovering(surface, ifc_model)
            if any(distance is not None and distance > 3 for distance in distances):
                print(f"  {surface.Name} filtered out due to exceeding ceiling distance.")
                continue

            # Vertical distance is the average of valid distances
            valid_distances = [d for d in distances if d is not None]
            if not valid_distances:
                print(f"  Cannot proceed without a valid ceiling height for {surface.Name}.")
                continue
            vertical_distance = sum(valid_distances) / len(valid_distances)
            print(f"  Average vertical distance to ceiling: {vertical_distance:.2f} m")

            # Classify surrounding surfaces (walls, windows, etc.)
            surrounding_areas = classify_surrounding_surfaces(surface, vertical_distance, ifc_model)

            # Calculate volume and absorption coefficients
            volume = top_surface_area * vertical_distance
            absorption_percentages, avg_absorption_coefficient = calculate_absorption_coefficients(surrounding_areas)

            # Calculate total surface area for reverberation time
            total_surface_area = sum(surrounding_areas.values()) + (top_surface_area * 2)  # Including floor and ceiling

            # Calculate reverberation time using Sabine's formula
            rt = calculate_reverberation_time(volume, avg_absorption_coefficient, total_surface_area)

            results.append({
                "name": surface.Name,
                "top_surface_area": top_surface_area,
                "vertical_distance": vertical_distance,
                "volume": volume,
                "absorption_percentages": absorption_percentages,
                "avg_absorption_coefficient": avg_absorption_coefficient,
                "reverberation_time": rt
            })

    return results

# Run the analysis and print results
results = analyze_all_floor_arc_surfaces(ifc_model)
print("\nFinal Results:")
for result in results:
    print(f"  {result['name']}:")
    print(f"    Top Surface Area: {result['top_surface_area']:.2f} m²")
    print(f"    Height to Ceiling: {result['vertical_distance']:.2f} m")
    print(f"    Volume: {result['volume']:.2f} m³")
    print(f"    Absorption Percentages: {', '.join([f'{k}: {v:.2f}%' for k, v in result['absorption_percentages'].items()])}")
    print(f"    Average Absorption Coefficient: {result['avg_absorption_coefficient']:.3f}")
    if result['reverberation_time'] is not None:
        print(f"    Reverberation Time: {result['reverberation_time']:.3f} s")
    else:
        print(f"    Reverberation Time: Cannot be calculated (average absorption coefficient is zero)")
