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

FILE_PATH = 'missing_api.txt'
OUTPUT_PATH = 'missing_api.dict'
uni_api_dict = {}

with open(FILE_PATH) as fp:
    for cnt, line in enumerate(fp):
        print("Line {}: {}".format(cnt, line))
        api = line.split(' ')[-1].strip("'")[:-2]
        if api.isdigit():
            continue
        if api not in uni_api_dict:
            uni_api_dict[api] = 0
        else:
            uni_api_dict[api] += 1

if __name__ == "__main__": 
    # ../dict/data.json
    json_file = convert_dict(sys.argv[1])
    with open(OUTPUT_PATH, "w") as outfile: 
        outfile.write(json_file) 
            