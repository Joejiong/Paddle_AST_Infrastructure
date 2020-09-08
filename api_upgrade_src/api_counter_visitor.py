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

import astor
import gast
import inspect
import os

from api_upgrade_src.node_operation import get_attr_full_name
from api_upgrade_src.upgrade_models_api_utils import print_info
from api_upgrade_src.upgrade_models_api_utils import load_counter_dict
from api_upgrade_src.upgrade_models_api_utils import save_counter_dict
from api_upgrade_src.common.Paths import SysPaths

COUNTER_DICT_PATH = './api_upgrade_src/dict/counter.dict'
COUNTER_OUTPUT_PATH_ORI = SysPaths.COUNTER_OUTPUT_PATH_ORI

# TODO(get general path before shell copy the tool)
# cwd = os.getcwd()
# cwd_prefix = "/".join([item for item in cwd.split('/') if item not in ["PaddleASTInfrastructure", "paddle_api_upgrade", "api_upgrade_src", "dict", "counter_output.dict"]])
# COUNTER_OUTPUT_PATH_ORI = cwd_prefix + '/PaddleASTInfrastructure/paddle_api_upgrade/api_upgrade_src/dict/counter_output.dict'



class APICountVisitor(gast.NodeTransformer):
    """
    APIVisitor will analyze any model repos, 
    to count how many Paddle api has been called.
    """
    def __init__(self, node):
        assert isinstance(node, gast.AST)
        self.root = node
        self.counter_dict = load_counter_dict(COUNTER_OUTPUT_PATH_ORI)
        self.modify_dict = {}

    def count_api_frequency(self, modify_dict): 
        self.modify_dict = modify_dict
        # self.counter_dict = counter_dict
        self.visit(self.root)

    def visit_Call(self, node): 
        self.generic_visit(node)
        attr_full_name = get_attr_full_name(node.func)
        if attr_full_name in self.modify_dict:
            self.counter_dict[attr_full_name]['count'] = self.counter_dict[attr_full_name].get('count', 0) + 1
            save_counter_dict(COUNTER_OUTPUT_PATH_ORI, self.counter_dict, attr_full_name)
            print_info("Counting old API once (%s)->hit No(%s) times" % (attr_full_name, self.counter_dict[attr_full_name]['count']))
        return node
