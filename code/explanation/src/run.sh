nohup>run1.log python -u run_instruct_following.py \
    --dataset ../data/200_tau-1.jsonl \
    --model PATH_TO_MODEL \
    --output ../results/llama3/tau-1/ \
    --cuda 4,5,6,7 &

nohup>run-1.log python -u run_instruct_following.py \
    --dataset ../data/200_tau1.jsonl \
    --model PATH_TO_MODEL \
    --output ../results/llama3/tau1/ \
    --cuda 4,5,6,7 &

nohup>run0.05.log python -u run_instruct_following.py \
    --dataset ../data/200_tau-0.05.jsonl \
    --model PATH_TO_MODEL \
    --output ../results/llama3/tau-0.05/ \
    --cuda 4,5,6,7 &