import unittest

import inspect
import gast
import astor
import codegen
import argparse
import sys
import paddle
from api_upgrade_src.modify_transformer import AddParamTransformer, DelParamTransformer, RenameParamTransformer, RepAttributeTransformer
from api_upgrade_src.replace_transformer import ReplaceTransformer
from api_upgrade_src.utils import load_replace_dict, load_modify_dict
from api_upgrade_src.main import main



def transformer(root, modify_dict): 
    AddParamTransformer(root).add(modify_dict)
    DelParamTransformer(root).delete(modify_dict)
    RenameParamTransformer(root).replace(modify_dict)
    RepAttributeTransformer(root).replace(modify_dict)
    return root
    

class TestNewApi(unittest.TestCase):
    
    maxDiff = None
    """
    test_add_kwarg
    test_delete_kwarg
    test_rename_kwarg
    test_fusion_def

    todo:
    test_single_model_file
    test_project_folder
    """
    def test_add_kwarg(self):
        # expected 
        expected = '''
def test1():
    data4 = paddle.tensor.zeros(x=x, shape=[3, 2], dtype='float32', out=None, device=None)
        '''
        # captured input
        input_test = '''
def test1():
    data4 = paddle.fluid.layers.zeros(x=x, shape=[3, 2], dtype='float32', force_cpu=True)
        '''

        # get captured 
        # root = gast.parse(inspect.getsource(input_test))
        root = gast.parse(input_test)
        root_expected = gast.parse(expected)
        print("*******test_1_source_code*******")
        # print(inspect.getsource(test1))
        root = transformer(root, modify_dict)
        print("*******test_add_kwarg*******")
        print(astor.to_source(gast.gast_to_ast(root)))
        captured = astor.to_source(gast.gast_to_ast(root))
        expected = astor.to_source(gast.gast_to_ast(root_expected))
        
        # testting
        self.assertEqual(expected, captured)

    def test_delete_kwarg(self):

        # expected 
        expected = '''
def test2(x, y):
    data4 = paddle.tensor.add(x, y, name=None, out=None, alpha=1)
        '''
        # captured input
        input_test = '''
def test2(x, y):
    data4 = paddle.fluid.layers.elementwise_add(x, y, axis=-1, act=None, name=None)
        '''

        # get captured 
        root = gast.parse(input_test)
        root_expected = gast.parse(expected)
        print("*******test_2_source_code*******")
        # print(inspect.getsource(test1))
        root = transformer(root, modify_dict)
        print("*******test_delete_kwarg*******")
        print(astor.to_source(gast.gast_to_ast(root)))
        captured = astor.to_source(gast.gast_to_ast(root))
        expected = astor.to_source(gast.gast_to_ast(root_expected))


        # testting
        self.assertEqual(expected, captured)

    def test_rename_kwarg(self):
        # expected 
        expected = '''
def test3(x, y):
    data4 = paddle.tensor.argmax(input=x, axis=2, out=None, dtype=None, keepdims=False, name=None)
        '''
        # captured input
        input_test = '''
def test3(x, y):
    data4 = paddle.fluid.layers.argmax(x=x, axis=2)
        '''

        # get captured 
        root = gast.parse(input_test)
        root_expected = gast.parse(expected)
        print("*******test_3_source_code*******")
        # print(inspect.getsource(test1))
        root = transformer(root, modify_dict)
        print("*******test_rename_kwarg*******")
        print(astor.to_source(gast.gast_to_ast(root)))
        captured = astor.to_source(gast.gast_to_ast(root))
        expected = astor.to_source(gast.gast_to_ast(root_expected))


        # testting
        self.assertEqual(expected, captured)

    def test_fusion_defDes(self):
        
        # expected 
        expected = '''
def test1(x):
    data1 = paddle.nn.data(x=x)
    data2 = paddle.tensor.reshape(x=data1, shape=[1, 2, 3])
    data4 = paddle.tensor.zeros(shape=[3, 2], dtype='float32', out=None, device=None)
    return abc
def test2(x): 
    data1 = paddle.tensor.tanh(input=x, out=None)
    data2 = paddle.tensor.zeros(shape=[3, 2], dtype='float32', out=None, device=None)
def test3(x): 
    data1 = paddle.nn.Sigmoid(x=x)
    data2 = paddle.tensor.sum(x, axis=0)
def test4(x): 
    data1 = paddle.tensor.max(input, dim=None, keep_dim=False, out=None, name=None)
    data2 = paddle.tensor.stack(x, dim=0, out=None)
    
        '''
        # captured input
        input_test = '''
def test1(x):
    data1 = paddle.fluid.layers.data(x=x)
    data2 = paddle.fluid.layers.reshape(x=data1, shape=[1, 2, 3])
    data3 = paddle.fluid.layers.zeros(shape=[3, 2], dtype='float32')
    data4 = paddle.fluid.layers.zeros(shape=[3, 2], dtype='float32', force_cpu=True)
    return abc
def test2(x): 
    data1 = paddle.fluid.layers.tanh(x=x)
    data2 = paddle.fluid.layers.zeros(shape=[3, 2], dtype='float32')
def test3(x): 
    data1 = paddle.fluid.layers.sigmoid(x=x)
    data2 = paddle.fluid.layers.reduce_sum(x, dim=0)
def test4(x): 
    data1 = paddle.fluid.layers.reduce_max(x=x)
    data2 = fluid.layers.stack(x, dim=0)
        '''

        # get captured 
        root = gast.parse(input_test)
        root_expected = gast.parse(expected)
        print("*******test_4_source_code*******")
        # print(inspect.getsource(test1))
        root = transformer(root, modify_dict)
        print("*******test_fusion_function_kwarg*******")
        print(astor.to_source(gast.gast_to_ast(root)))
        captured = astor.to_source(gast.gast_to_ast(root))
        expected = astor.to_source(gast.gast_to_ast(root_expected))

        # testting
        self.assertEqual(expected, captured)


    def test_single_model_file(self):

        parser = argparse.ArgumentParser("Paddle API upgrade")
        parser.add_argument("--modify_dict", type=str, default="../dict/modify.dict")
        parser.add_argument("--input", type=str, default='./class_cnn.py')
        parser.add_argument("--output", type=str, default='./class_cnn_update.py')
        args = parser.parse_args()
    
        main(args)
        # read captured
        
        with open('./class_cnn_update.py', 'r') as fp:
            data_captured = fp.read()
        
        with open('./class_cnn_expected.py', 'r') as fp:
            data_expected = fp.read()


        # expected 
        expected = data_expected
        # captured input
        input_test = data_captured

        # # get captured 
        # root = gast.parse(input_test)
        # root_expected = gast.parse(expected)
        # print("*******test_5_source_code*******")
        # # print(inspect.getsource(test1))
        # root = transformer(root, modify_dict)
        print("*******test_model_single_file*******")
        # print(astor.to_source(gast.gast_to_ast(root)))
        # captured = astor.to_source(gast.gast_to_ast(root))
        # expected = astor.to_source(gast.gast_to_ast(root_expected))


        # testting
        self.assertEqual(data_expected, data_captured)
    
    def test_project_folder(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    modify_dict = load_modify_dict('../dict/modify.dict')
    unittest.main()
