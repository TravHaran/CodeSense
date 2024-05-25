import os
import json

def create_folder_structure_json(path):
    # Initialize the result dictionary with folder
    # name, type, and an empty list for children
    result = {'name': os.path.basename(path),
              'type': 'folder', 'children': []}
    
    # Check if the path is a directory
    if not os.path.isdir(path):
        return result
    
    # Iterate over the entries in the directory
    for entry in os.listdir(path):
        if not entry.startswith('.'): # ignore hidden folders & files
            # Create the full path for current entry
            entry_path = os.path.join(path, entry)
            
            #if the entry is a directory, recursively call the function
            if os.path.isdir(entry_path):
                result['children'].append(create_folder_structure_json(entry_path))
            # if the entry is a file, create a dictionary with name and type
            else:
                # save file content as string
                try:
                    content = file_to_string(entry_path)
                except OSError:
                    content = "n/a"
                result['children'].append({'name': entry, 'type': 'file', 'content': content})
    return result

def file_to_string(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    file.close()
    return file_content
# Specify the path to the folder you want to create the JSON for
folder_path = '/Users/trav/Documents/projects/codesense'

# Call the function to create the JSON representation
folder_json = create_folder_structure_json(folder_path)

# Convert the dictionary to a JSON string with indentation
folder_json_str = json.dumps(folder_json, indent=4)

# Print the JSON representation of the folder structure
print(folder_json_str)

# Save as a JSON file
save_file = open("codebase.json", 'w')
json.dump(folder_json, save_file, indent=4)
save_file.close()


    