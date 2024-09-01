import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse

def create_path(stroke):
    path = ""
    for i, point in enumerate(stroke):
        if i == 0:
            path += f"M{point['p0'][0]},{point['p0'][1]} "
        path += f"C{point['p1'][0]},{point['p1'][1]} {point['p2'][0]},{point['p2'][1]} {point['p3'][0]},{point['p3'][1]} "
    return path

def json_to_svg(json_data):
    # Parse JSON data
    data = json.loads(json_data)

    # Create SVG element
    svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg")

    # Initialize min/max coordinates
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    # Compute the bounding box by checking all stroke points
    for stroke_group in data['strokes']:
        for stroke in stroke_group:
            for point in ['p0', 'p1', 'p2', 'p3']:
                x, y = stroke[point][0], stroke[point][1]
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)

    # Calculate width and height
    width = max_x - min_x
    height = max_y - min_y

    # Set the viewBox to include all strokes
    svg.set('viewBox', f"{min_x} {min_y} {width} {height}")

    # Create a group element with transform to flip vertically
    group = ET.SubElement(svg, 'g', transform=f"scale(1, -1) translate(0, {-max_y - min_y})")

    # Create path for each stroke group
    for stroke_group in data['strokes']:
        path = ET.SubElement(group, 'path')
        path.set('d', create_path(stroke_group))
        path.set('fill', 'none')
        path.set('stroke', 'black')
        path.set('stroke-width', '60')
        path.set('stroke-linecap', 'round')

    # Convert to string and pretty print
    xml_str = ET.tostring(svg, encoding='unicode')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

    return pretty_xml_str

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert JSON stroke data to SVG')
    parser.add_argument('input', help='Input JSON file path')
    parser.add_argument('output', help='Output SVG file path')

    # Parse arguments
    args = parser.parse_args()

    # Read input file
    with open(args.input, 'r') as file:
        json_data = file.read()

    # Convert JSON to SVG
    svg_output = json_to_svg(json_data)

    # Write output file
    with open(args.output, 'w') as file:
        file.write(svg_output)

    print(f"SVG file has been created as '{args.output}'")

if __name__ == "__main__":
    main()
