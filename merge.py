import xml.etree.ElementTree as ET
import os
import pprint
# List of your XML input files
input_files = [
    "Block-Lists_scammers-AVM_and_other_ROUTERS-2026-07-20.xml",
    "Telefonbuch_Rufsperren_1202-2026-07-20.xml",
    "FRITZ.Box_Telefonbuch_Call-Center_Werbeanrufe.xml",
    "FRITZ.Box_Telefonbuch_Rufsperren_beautify.xml",
    "FB_Telefonbuch_Spam_2025.xml",
    "Telefonbuch_Rufsperren_BlueBox_FRITZ.Box_17.06.25_1649.xml"
]

output_file = "Merged_Blocklist_FRITZBox.xml"

# Check if the primary base file exists
if not os.path.exists(input_files[0]):
    print(f"Error: Base file '{input_files[0]}' not found.")
    exit(1)

print(f"Loading base structure from: {input_files[0]}")
# Load the first file to preserve the correct FRITZ!Box XML header format
main_tree = ET.parse(input_files[0])
main_root = main_tree.getroot()

# Locate the actual phonebook sub-element (usually <phonebook>)
main_phonebook = main_root.find('phonebook')

if main_phonebook is None:
    print("Error: Could not find <phonebook> element in the base file.")
    exit(1)

# Extract contacts from the remaining files and append them
for file_name in input_files[1:]:
    if os.path.exists(file_name):
        try:
            tree = ET.parse(file_name)
            root = tree.getroot()
            phonebook = root.find('phonebook')
            
            if phonebook is not None:
                contact_count = 0
                for contact in phonebook.findall('contact'):
                    main_phonebook.append(contact)
                    contact_count += 1
                print(f"Successfully appended {contact_count} contacts from: {file_name}")
            else:
                print(f"Warning: No <phonebook> element found in: {file_name}")
        except ET.ParseError:
            print(f"Error: Failed to parse XML file: {file_name}")
    else:
        print(f"Warning: File not found, skipping: {file_name}")

# Save the combined data into a single file
try:
    main_tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"\nSuccess! The merged file has been saved as '{output_file}'.")
except Exception as e:
    print(f"Error saving output file: {e}")