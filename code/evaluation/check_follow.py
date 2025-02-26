import os
import argparse
import sys
import pandas as pd

import instructions_registry

sys.path.append('../')
import utils


parser = argparse.ArgumentParser()
parser.add_argument('--model_name', type=str, default='llama3')
parser.add_argument('--result_dir', type=str, default='../data/results/')
parser.add_argument('--save_dir', type=str, default='./check_follow.xlsx')
args = parser.parse_args()

_, _, files = next(os.walk(args.result_dir))

total_res = []
for f in files:
    datas = utils.readjsonl(args.result_dir + f)
    res = []
    follow_cons_list = {}
    follow_inst_list = {}
    follow_inst_list.setdefault('correct', 0)
    follow_inst_list.setdefault('total', 0)
    for data in datas:
        ids_to_check = data['instruction_id_list']
        args_to_check = data['kwargs']
        resp_to_check = data['response']

        if type(resp_to_check) != str:
           resp_to_check = ""        


        is_following_list = []
        for ids, arg in zip(ids_to_check, args_to_check):
            instruction_cls = instructions_registry.INSTRUCTION_DICT[ids]
            instruction = instruction_cls(ids)
            instruction.build_description(**arg)
            
            if resp_to_check.strip() and instruction.check_following(resp_to_check):
                is_following_list.append(True)
                follow_cons_list.setdefault(ids.split(':')[0], {}).setdefault('correct', 0)
                follow_cons_list[ids.split(':')[0]]['correct'] += 1
            else:
                is_following_list.append(False)


            follow_cons_list.setdefault(ids.split(':')[0], {}).setdefault('total', 0)
            follow_cons_list[ids.split(':')[0]]['total'] += 1
        if all(is_following_list):
            follow_all_cons = True
            follow_inst_list['correct'] += 1
        else:
            follow_all_cons = False
        follow_inst_list['total'] += 1

        data['follow_all_cons'] = follow_all_cons
        data['follow_cons_list'] = is_following_list
        res.append(data)

    follow_result = {}
    constraint_level = 0
    cons_correct = 0
    cons_total = 0
    for k,v in follow_cons_list.items():
        cons_correct += v.get('correct', 0)
        cons_total += v['total']
        follow_result[k] = v.get('correct', 0) / v['total']

    follow_result['constraint_level'] = cons_correct / cons_total
    follow_result['instruction_level'] = follow_inst_list['correct'] / follow_inst_list['total']

    total_res.append(follow_result)
    # print(follow_result)


model_name = args.model_name
index_name = [f.split('_response')[0] for f in files]
index_name = [f.split('{}tau'.format(model_name))[-1] for f in index_name]


df = pd.DataFrame(total_res, index=index_name)
df.to_excel(args.save_dir, index_label='position')
        