"""
Creates a baseline valid single-class YOLO ONNX detection model graph
matching YOLOv8/v11 input/output architecture for Edge AI inference.
Input: 'images' [1, 3, 640, 640]
Output: 'output0' [1, 5, 8400] (cx, cy, w, h, enclosure_conf)
"""

import os
import numpy as np
import onnx
from onnx import helper, TensorProto

def create_base_yolo_onnx(output_path="models/enclosure_detector_base.onnx"):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Define inputs and outputs
    X = helper.make_tensor_value_info('images', TensorProto.FLOAT, [1, 3, 640, 640])
    Y = helper.make_tensor_value_info('output0', TensorProto.FLOAT, [1, 5, 8400])
    
    # Create lightweight convolutional and feature extraction layers
    # Conv1: 3 -> 8 channels, 3x3 kernel
    w_conv1 = np.random.randn(8, 3, 3, 3).astype(np.float32) * 0.05
    b_conv1 = np.zeros(8, dtype=np.float32)
    node_w1 = helper.make_tensor('w_conv1', TensorProto.FLOAT, [8, 3, 3, 3], w_conv1.flatten().tolist())
    node_b1 = helper.make_tensor('b_conv1', TensorProto.FLOAT, [8], b_conv1.tolist())
    
    conv1 = helper.make_node('Conv', ['images', 'w_conv1', 'b_conv1'], ['conv1_out'],
                             kernel_shape=[3, 3], pads=[1, 1, 1, 1])
    relu1 = helper.make_node('Relu', ['conv1_out'], ['relu1_out'])
    
    # Global average pool: [1, 8, 640, 640] -> [1, 8, 1, 1]
    pool = helper.make_node('GlobalAveragePool', ['relu1_out'], ['pool_out'])
    
    # Dense linear projection to output [1, 5, 8400]
    # Flatten pool_out to [1, 8]
    flatten = helper.make_node('Flatten', ['pool_out'], ['flat_out'])
    
    # Project to 5 * 8400 = 42,000 dimensions
    w_fc = np.random.randn(8, 42000).astype(np.float32) * 0.001
    b_fc = np.zeros(42000, dtype=np.float32)
    # Set bias for enclosure confidence to reasonable starting logit
    b_fc.reshape(5, 8400)[4, :] = 0.05
    # Center boxes
    b_fc.reshape(5, 8400)[0, :] = 320.0
    b_fc.reshape(5, 8400)[1, :] = 320.0
    b_fc.reshape(5, 8400)[2, :] = 160.0
    b_fc.reshape(5, 8400)[3, :] = 120.0
    
    node_w_fc = helper.make_tensor('w_fc', TensorProto.FLOAT, [8, 42000], w_fc.flatten().tolist())
    node_b_fc = helper.make_tensor('b_fc', TensorProto.FLOAT, [42000], b_fc.flatten().tolist())
    
    matmul = helper.make_node('MatMul', ['flat_out', 'w_fc'], ['matmul_out'])
    add_bias = helper.make_node('Add', ['matmul_out', 'b_fc'], ['fc_out'])
    
    # Reshape to [1, 5, 8400]
    shape_tensor = helper.make_tensor('out_shape', TensorProto.INT64, [3], [1, 5, 8400])
    reshape = helper.make_node('Reshape', ['fc_out', 'out_shape'], ['output0'])
    
    graph = helper.make_graph(
        [conv1, relu1, pool, flatten, matmul, add_bias, reshape],
        'yolo_enclosure_detector',
        [X],
        [Y],
        [node_w1, node_b1, node_w_fc, node_b_fc, shape_tensor]
    )
    
    model = helper.make_model(graph, producer_name='EdgeAI_M1_RMCS610', opset_imports=[helper.make_opsetid('', 17)])
    model.ir_version = 9
    onnx.checker.check_model(model)
    onnx.save(model, output_path)
    print(f"[+] Successfully constructed verified YOLO ONNX base model: {output_path}")

if __name__ == "__main__":
    create_base_yolo_onnx()
