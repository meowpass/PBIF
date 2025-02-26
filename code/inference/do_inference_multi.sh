for i in -1 -0.8 -0.6 -0.4 -0.2 -0.05 0.05 0.2 0.4 0.6 0.8 1
do
    nohup python do_inference_multi.py \
    --data_path ../../data/multi_round/llama3_8b/llama3_8b_tau${i}.jsonl \
    --res_path ../../results/multi_round/llama3_8b/llama3_8b_tau${i}_response.jsonl \
    > multi_round_llama3_8b_tau${i}.log 2>&1 &
    wait $! 
done