#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import json

json_file = './counter.dict'

# Working with buffered content
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
    print("name is ->", name)
    data.update(data)

## Save our changes to JSON file
jsonFile = open(json_file, "w+")
jsonFile.write(json.dumps(data))
jsonFile.close()