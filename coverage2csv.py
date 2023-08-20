import xml.etree.ElementTree as ET
import csv

# Parse the XML report
tree = ET.parse('coverage.xml')
root = tree.getroot()

# Extract coverage data
coverage_data = []
for package in root.findall('.//package'):
    coverage_data.append({
        'name': package.attrib['name'],
        'coverage': package.attrib['line-rate']
    })

# Write data to CSV
with open('coverage.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'coverage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in coverage_data:
        writer.writerow(row)
