import sys


if sys.version_info >= (3, 9):
    from importlib.resources import files
else:
    from importlib_resources import files
from multilayer_perceptron import resources

def load_mlp():
    import onnxruntime as rt

    sess = rt.InferenceSession(
        files(resources).joinpath("trained_mlp_vanthoff_etal_2026.onnx"), providers=["CPUExecutionProvider"]
    )
    return sess