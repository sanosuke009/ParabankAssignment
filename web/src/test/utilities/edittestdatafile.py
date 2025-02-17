import json

def edit_json_file(file_path, field, field2, new_value):
    with open(file_path, 'r') as file:
        data = json.load(file)
    data[field][field2] = new_value
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)