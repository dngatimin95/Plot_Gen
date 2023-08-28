import gpt_2_simple as gpt2
from tensorflow.python.compiler.tensorrt import trt_convert as trt
from transformers import (
    GPT2Tokenizer,
    DataCollatorForLanguageModeling,
    TextDataset,
    GPT2LMHeadModel,
    TrainingArguments,
    Trainer,
    pipeline)

file_name = "summary.txt"
#split summary txt to train and test subtexts

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=train_path,
    block_size=128)
     
test_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=test_path,
    block_size=128)
     
print(tokenizer.decode(train_dataset[5]))

model = GPT2LMHeadModel.from_pretrained('gpt2')

training_args = TrainingArguments(
    output_dir = 'data/out', # output directory for the model predictions and checkpoints
    overwrite_output_dir = True, # overwrite content of the output directory
    per_device_train_batch_size = 32, # batch size for training
    per_device_eval_batch_size = 32, # batch size for evaluation
    learning_rate = 5e-5, # default learning rate
    num_train_epochs = 3, # total number of epochs to perform
)

trainer = Trainer(
    model = model,
    args = training_args,
    data_collator=data_collator,
    train_dataset = train_dataset,
    eval_dataset = test_dataset
)

trainer.train()
trainer.save_model()

generator = pipeline('text-generation', tokenizer='gpt2', model='data/out')

print(generator('', max_length=40)[0]['generated_text'])
