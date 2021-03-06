import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.python.framework import graph_util


class OpGenerator:
    def __init__(self, shape, num_or_size_splits, axis, tflite_dtype=tf.float32):
        self.shape = shape
        self.axis = axis
        self.num_or_size_splits = num_or_size_splits
        self.tflite_dtype = tflite_dtype
        self.name = "split"
        self.iname = "input"
        self.oname = "output"

    def genTensorFlowModel(self):
        print("Generating TensorFlow model...")
        with tf.Session(graph=tf.Graph()) as sess:
            net = tf.placeholder(self.tflite_dtype, shape=self.shape, name=self.iname)
            net = tf.split(net, num_or_size_splits=self.num_or_size_splits, axis=self.axis, name=self.oname)
            sess.run(tf.global_variables_initializer())
            constant_graph = graph_util.convert_variables_to_constants(
                sess, sess.graph_def, [self.oname])
            with tf.gfile.FastGFile(self.name + ".pb", mode='wb') as f:
                f.write(constant_graph.SerializeToString())

    def genTFLiteModel(self):
        print("Generating TensorFlow Lite model...")
        converter = tf.lite.TFLiteConverter.from_frozen_graph(
            self.name + ".pb",
            input_arrays=[self.iname],
            output_arrays=[self.oname, ])
        converter.inference_type = self.tflite_dtype
        converter.inference_inpute_type = self.tflite_dtype
        # converter.default_ranges_stats = (0, 6)
        # converter.quantized_input_stats = {self.iname: (100, 100.0)}

        # converter.post_training_quantize = True
        # converter.target_ops = set([OpsSet.TFLITE_BUILTINS])

        tflite_model = converter.convert()
        open(self.name + ".tflite", "wb").write(tflite_model)


def genOP():
    print("[START] genOP\n")
    print("TensorFlow: %s" % tf.__version__)

    shape = (1, 4, 4, 9)
    num_or_size_splits = (1, 3, 5)
    axis = -1

    tflite_dtype = tf.float32

    op = OpGenerator(shape, num_or_size_splits, axis, tflite_dtype=tflite_dtype)
    op.genTensorFlowModel()
    op.genTFLiteModel()

    print("\n[DONE] genOP")


genOP()
