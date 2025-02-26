CUDA_VISIBLE_DEVICES=0,1,2,3 nohup>server.log python -m vllm.entrypoints.openai.api_server \
  --model PATH_TO_MODEL \
  --port 8105 \
  --tensor-parallel-size 4 \
  --disable-log-requests