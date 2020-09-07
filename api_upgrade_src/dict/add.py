import json

json_file = './counter.dict'

 ## Working with buffered content
jsonFile = open(json_file, "r") # Open the JSON file for reading
data = json.load(jsonFile) # Read the JSON into the buffer
jsonFile.close() # Close the JSON file

add_dict = {}

for key in data: 
    value = data[key]
    if key.startswith("paddle."): 
        key = key.lstrip("paddle.")
        add_dict[key] = value
        add_dict[key].get("count", 0)
    if key.startswith("fluid."): 
        key = key.lstrip("fluid.")
        add_dict[key] = value
        add_dict[key].get("count", 0)
    data.update(add_dict)
    print("name is ------------------------->", name)
    # data[name].get("count", 0)
    data.update(data)
# print(json_object[name]["count"])

## Save our changes to JSON file
jsonFile = open(json_file, "w+")
jsonFile.write(json.dumps(data))
jsonFile.close()