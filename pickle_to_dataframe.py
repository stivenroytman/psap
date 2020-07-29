import pickle
import pandas
import glob
import os
import numpy as np
from misc_functions import *

def get_dump_latency(dump_data):
    dump_list = list()
    sum_latency = 0
    for dump in dump_data:
        if dump[2] == 'NA': continue
        else: dump_list.append(dump[2])
    for dump in dump_list: sum_latency += dump
    if len(dump_list) == 0: return 'NA'
    average_latency = sum_latency / len(dump_list)
    return average_latency

def empty_data_dictionary(num_blocks):
    data_dict = {}
    for n in range(num_blocks):
        data_dict[str(n+1)]={}
        data_dict[str(n+1)]['name']=[]
        data_dict[str(n+1)]['press_1']=[]
        data_dict[str(n+1)]['press_2']=[]
        data_dict[str(n+1)]['press_3']=[]
        data_dict[str(n+1)]['points']=[]
        data_dict[str(n+1)]['provoked']=[]
        data_dict[str(n+1)]['dump_latency']=[]
        data_dict[str(n+1)]['defense_rewards']=[]
    return data_dict

def get_pickle_dictionary():
    pickle_dictionary = {}
    pickle_addresses = glob.glob(os.path.join("Data", "pickle", "*.pickle"))
    for data in pickle_addresses:
        pickle_dictionary[data.split('_')[0]] = pandas.read_pickle(data)
    return pickle_dictionary

def fill_data_dict(empty_dict, pickle_dict):
    data_dict = empty_dict
    pickle_dictionary = pickle_dict
    for data in pickle_dictionary:
        for block in pickle_dictionary[data]:
            data_dict[block]['name'].append(data)
            data_dict[block]['press_1'].append(pickle_dictionary[data][block]['total_presses']['1'])
            data_dict[block]['press_2'].append(pickle_dictionary[data][block]['total_presses']['2'])
            data_dict[block]['press_3'].append(pickle_dictionary[data][block]['total_presses']['3'])
            data_dict[block]['points'].append(pickle_dictionary[data][block]['player_points'])
            data_dict[block]['provoked'].append(pickle_dictionary[data][block]['player_provoked'])
            data_dict[block]['dump_latency'].append(get_dump_latency(pickle_dictionary[data][block]['dumps']))
            data_dict[block]['defense_rewards'].append(np.mean(pickle_dictionary[data][block]['defense_rewards']))
    return data_dict

def get_dataframe_list(tidy_data):
    dataframe_list = []
    for block in tidy_data:
        globals()['output_csv_' + block] = pandas.DataFrame()
        for metric in tidy_data[block]:
            globals()['output_csv_' + block][metric] = tidy_data[block][metric]
        dataframe_list.append(globals()['output_csv_' + block])
    return dataframe_list

test_data = fill_data_dict(empty_data_dictionary(3), get_pickle_dictionary())

test_list = get_dataframe_list(test_data)

writer = pandas.ExcelWriter(os.path.join('Data', 'excel', 'global_data.xlsx'), engine = 'xlsxwriter')
for n in range(len(test_list)):
    sheet = 'df_block_' + str(n+1)
    test_list[n].to_excel(writer, sheet_name = sheet)
writer.save()


