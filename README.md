# BMKMPHI
Run this code to train the model.

lr=1e-5
epoch=150
batch_size=32
margin=1

device="cuda:0"
CODE="train_cl.py"
kmer=6
model="CNN"
model_save_path="model_save_path/" 
model_info="CL_model_margin-{$margin}-epoch-${epoch}" 


# host data
host_fa="data/host.fasta"
host_list="data/species.txt"

# phage data
train_phage_fa="data/train.fasta"
train_host_gold="data/ytraun.csv"
valid_phage_fa="data/val.fasta"
valid_host_gold="data/yval.csv"

python $CODE --model $model --model_dir $model_save_path/${model_info}.pth --kmer $kmer --margin $margin \
	--host_fa $host_fa --host_list $host_list \
	--train_phage_fa $train_phage_fa  --train_host_gold $train_host_gold \
	--valid_phage_fa $valid_phage_fa  --valid_host_gold  $valid_host_gold \
	--device $device --lr $lr --epoch $epoch --batch_size $batch_size 




Run this code for testing after training is complete.


lr=1e-5
batch_size=32
margin=1
device="cuda:0"
kmer=6
model="CNN"
model_file="model_save_path/CL_model_margin-{1}-epoch-150.pth"
OUTPUT="results/CL4PHI_pred_results.txt"

host_fa="data/host.fasta"
host_list="data/species.txt"
test_phage_fa="data/test.fasta"
test_host_gold="data/ytest.csv"

python eval.py --model "CNN" --model_dir $model_file \
 --host_fa $host_fa --host_list $host_list \
 --test_phage_fa $test_phage_fa \
--test_host_gold $test_host_gold \
 --kmer $kmer --device $device
