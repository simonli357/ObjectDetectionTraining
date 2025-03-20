import onnx

# Path to your ONNX model file
onnx_model_path = 'C:/Users/simon/Downloads/linxy/YOLOv8/try3_26/detect/train/weights/best.onnx'

# Load the ONNX model
model = onnx.load(onnx_model_path)

# Display information about the model outputs
print("Output shapes:")
for i, output in enumerate(model.graph.output):
    shape = [dim.dim_value for dim in output.type.tensor_type.shape.dim]
    print(f"Output {i + 1}: Shape {shape}")


# import tensorrt as trt

# # Load the serialized TensorRT engine
# engine_path = 'C:/Users/simon/Downloads/linxy/YOLOv8/try3_26/detect/train/weights/best.engine'
# with open(engine_path, 'rb') as f, trt.Runtime(trt.Logger()) as runtime:
#     engine_data = f.read()
#     engine = runtime.deserialize_cuda_engine(engine_data)

# # Get information about the engine's bindings (inputs and outputs)
# output_shapes = []
# for i in range(engine.num_bindings):
#     # if engine.binding_is_output(i):
#     shape = engine.get_binding_shape(i)
#     dtype = engine.get_binding_dtype(i)
#     output_shapes.append((shape, dtype))

# # Output information about output bindings (shapes and types)
# print("Output shapes and types:")
# for i, (shape, dtype) in enumerate(output_shapes):
#     print(f"Output {i + 1}: Shape {shape}, Type {dtype}")
