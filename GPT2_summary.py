import gpt_2_simple as gpt2
from tensorflow.python.compiler.tensorrt import trt_convert as trt

model_name= "124M"

if not os.path.isdir(os.path.join("models", model_name)):
	gpt2.download_gpt2(model_name=model_name)


file_name = "summary.txt"
sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              steps=1000)   # steps is max number of training steps

gpt2.generate(sess)
