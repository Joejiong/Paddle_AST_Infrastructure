import paddle
import paddle.fluid as fluid
import numpy as np
from paddle.fluid.dygraph.nn import Linear
from paddle.fluid.dygraph.base import to_variable

class MNIST(fluid.dygraph.Layer):
    def __init__(self, name_scope):
        super(MNIST, self).__init__(name_scope)
        self.fc = Linear(input_dim=784, output_dim=1, act=None)

    def forward(self, inputs):
        
        inputs = paddle.fluid.layers.data(input)
        inputs = paddle.fluid.layers.reshape(inputs, (-1, 784))
        zeros = paddle.fluid.layers.zeros(shape=[1, 2], dtype="float32", force_cpu=False)
        
        inputs = paddle.fluid.layers.Linear(700, 400)
        outputs = self.fc(inputs)
        return outputs