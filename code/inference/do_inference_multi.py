from openai import OpenAI
from tqdm import tqdm
import threading
import json
import concurrent.futures
import argparse
from threading import Lock

def writejsonl(data, datapath):
    with open(datapath, "a", encoding='utf-8') as f:
        for item in data:
            json_item = json.dumps(item, ensure_ascii=False)
            f.write(json_item + "\n")
def writejson(data, json_path):
    json_str = json.dumps(data, ensure_ascii=False)
    with open(json_path, "a", encoding='utf-8') as json_file:
        json_file.write(json_str)
        json_file.write('\n')
def readjsonl(datapath):
    res = []
    with open(datapath, "r", encoding='utf-8') as f:
        for line in f.readlines():
            # print(line)
            res.append(json.loads(line))
    return res
def readjson(datapath):
    with open(datapath, "r", encoding='utf-8') as f:
        res = json.load(f)
    return res


def generate_response(data):
    
    openai_api_base = "http://localhost:8105/v1"
    openai_api_key = "EMPTY"
    
    client = OpenAI(base_url=openai_api_base, api_key=openai_api_key) 
    history = []
    history.append({"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"})
    
    initial_prompt = data['prompt']
    history.append({"role": "user","content": initial_prompt})
    
    response = client.chat.completions.create(
        model=client.models.list().data[0].id,
        messages= history
    )
    response = response.choices[0].message.content 
    history.append({"role": "assistant","content": response})
    
    for cons in data['constraints']:
        history.append({"role": "user","content": cons+"."})
        response = client.chat.completions.create(
            model=client.models.list().data[0].id,
            messages= history
        )
        response = response.choices[0].message.content 
        history.append({"role": "assistant","content": response})
    
    res = {
        "prompt" : data['prompt'],
        "instruction_id_list": data['instruction_id_list'],
        "kwargs": data['kwargs'],
        "constraints" :data['constraints'],
        "ranking": data['ranking'],
        "history": history,
        "response": response
    }
    print(response)
    return res


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path",type=str, required=True, default='',help="data path")
    parser.add_argument("--res_path",type=str, required=True, default='',help="res path")
    args = parser.parse_args()
    
    data_path = args.data_path
    res_path = args.res_path
    datas = readjsonl(data_path)
    
    
    write_lock = Lock()  # global lock
    
    
    
    # Define the number of threads
    num_threads = 50 
    res_batch = 5

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks for each data sample
        futures = [executor.submit(generate_response, data) for data in datas]

        res = []
        # Optionally collect the results
        for future in concurrent.futures.as_completed(futures):
            try:
                one_res = future.result()
                res.append(one_res)
                if len(res) > res_batch:
                    with write_lock:
                        writejsonl(res,res_path)
                        res.clear()
                
            except Exception as e:
                print(f"An error occurred: {e}")
        
        with write_lock:
            writejsonl(res,res_path) 
