# Order Matters: Investigate the Position Bias in Multi-constraint Instruction Following

[![Github](https://img.shields.io/static/v1?logo=github&style=flat&color=pink&label=github&message=meowpass/FollowComplexInstruction)]([https://github.com/meowpass/PBIF](https://github.com/meowpass/PBIF))
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-huggingface-yellow)](https://huggingface.co/datasets/Abbey4799/Complex-Instructions-DPO)

Official implementation of the paper "Order Matters: Investigate the Position Bias in Multi-constraint Instruction Following". 

We systematically study **the position bias problem in multi-constraint
instruction following**. Through our experiments, we have the following findings:

- **LLMs prefer to "hard-to-easy" constraint order**
  - existing LLMs can achieve a better following accuracy in multi-constraint instructions when presented with constraints in “hard-to-easy” orders. 
  - This finding can be generalized in both single-round and multi-round scenarios, regardless of the architecture of LLM, the size of LLM’s parameters and the number of constraints.
- **Constraints order affect how the LLMs handle a specific constraint**
  - The "Hard-to-easy" constraint order induces the LLM to pay more attention to the constraint part in the multi-constraint instructions.
  - The LLM’s performance on various constraints is strongly correlated with its attention patterns.


![图片14](https://github.com/user-attachments/assets/d6c641de-60df-4d93-9ba4-515929b4e1b4)


## 🔥Updates

* 2025/2/26: We released the data and code of PBIF

## ⚙️How to Use the Code

### Install Dependencies

```
conda create -n pbif python=3.10.9
conda activate pbif
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
pip install -r requirements.txt
```

### Inference

we leverage the vLLM to accelerate our inference. First, you can deploy a local model by running the script `deploy_model.sh`:

```python
CUDA_VISIBLE_DEVICES=0,1,2,3 nohup>server.log python -m vllm.entrypoints.openai.api_server \
  --model PATH_TO_MODEL \
  --port 8105 \
  --tensor-parallel-size 4 \
  --disable-log-requests
```



#### Single-round inference

We provide an example to do inference with LLaMA3_8B_Inst model. You can adjust corresponding setting (e.g., system prompt, temperature) to introduce your model. For LLaMA3_8B_Inst model, just run the script `do_inference_single.sh`

```shell
for i in -1 -0.8 -0.6 -0.4 -0.2 -0.05 0.05 0.2 0.4 0.6 0.8 1
do
    nohup python do_inference_single.py \
    --data_path ../../data/single_round/llama3_8b/llama3_8b_tau${i}.jsonl \
    --res_path ../../results/single_round/llama3_8b/llama3_8b_tau${i}_response.jsonl \
    > single_round_llama3_8b_tau${i}.log 2>&1 &
    wait $! 
done
```




#### Multi-round inference

Similarly, we provide a script in `do_inference_multi.sh`

```shell
for i in -1 -0.8 -0.6 -0.4 -0.2 -0.05 0.05 0.2 0.4 0.6 0.8 1
do
    nohup python do_inference_multi.py \
    --data_path ../../data/multi_round/llama3_8b/llama3_8b_tau${i}.jsonl \
    --res_path ../../results/multi_round/llama3_8b/llama3_8b_tau${i}_response.jsonl \
    > multi_round_llama3_8b_tau${i}.log 2>&1 &
    wait $! 
done
```



### Evaluation

Since the evaluation is based on rules, you can readily evaluate the model performance on different types of constraints. We provide a script `check_follow.sh` in \code\evaluation:

```shell
python check_follow.py \
    --model_name llama3 \
    --result_dir ../../results/single_round/llama3_8b/ \
    --save_dir ../../results/follow_results/llama3_8b_single_round.xlsx \

python check_follow.py \
    --model_name llama3 \
    --result_dir ../../results/multi_round/llama3_8b/ \
    --save_dir ../../results/follow_results/llama3_8b_multi_round.xlsx \
```

### Explanation

We also provide the codes to visualize the importance of different constraints. The code is based on the paper [JacksonWuxs/Interpret_Instruction_Tuning_LLMs: Understanding Why and How Instruction Tuning Changes Pre-trained Models](https://github.com/JacksonWuxs/Interpret_Instruction_Tuning_LLMs) (Thanks for their work). For a quick use, run the script `run.sh` in /code/explanation/src/:

```python
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
```



## Citation

```

```
