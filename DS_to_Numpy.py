import ROOT 
import numpy as np
import os

# input: 
# dataset - initial dataset
# var_lst - name of variables to add in numpy array 
#ds = DS_to_Numpy(data, ['evt', 'run'])
#ds = DS_to_Numpy_for_old_version(data, ['evt', 'run']) - for old ROOT package version
# output: 
# data - numpy array with values of the required variables

def DS_to_Numpy_for_old_version(dataset, var_lst): 
    store = dataset.store()
    n = store.size()
    vars = dataset.get()

    if not isinstance(store, ROOT.RooVectorDataStore):
        if isinstance(store, ROOT.RooTreeDataStore):
            dataset.ConvertToVectorStore()
        else:
            variables = store.get()
            store_name = store.GetName()
            tmp_store = ROOT.RooVectorDataStore(store, variables, store_name)
        
    # using numpy structed array
    data = np.zeros(n, dtype={'names': (var_lst), 'formats':('f8', 'f8', (n ,len(var_lst)))})

    # for large datasets
    # check batch size * var size < 10^6 
    num_entries = store.numEntries()
    count_vars = len(vars)
    data_limit = num_entries * count_vars
    num_limit = 1000000
    nb,r = divmod(n, num_limit)

    if data_limit < num_limit:
        array_info = store.getBatches(0, n)
        count = 0
        for x in array_info:
            if vars[count].GetName() in var_lst:
                data[vars[count].GetName()] = x.second
            count = count + 1
    else: 
        rargs = [(i*num_limit, num_limit) for i in range(nb)] + [(nb * num_limit,r)]
        print(rargs)
        data_part = []
        for first, num in rargs:
            array_info = store.getBatches(first, num)
        #for i in range(0, n, num_limit):
        #    if i == n - remainder:
        #        array_info = store.getBatches(i, remainder)
        #    else:
        #        array_info = store.getBatches(i, num_limit)
            count = 0
            for x in array_info:
                if vars[count].GetName() in var_lst:
                    data_part.append(str(x.second))
                    #print(data_part)
                count = count + 1
        data_np = np.array(data_part, dtype= object)
        
        print(len(data_np))
        print(data_np[0])
    return data_np


def DS_to_Numpy_for_new_version(dataset, var_lst):
    store = dataset.store()

    if not isinstance(store, ROOT.RooVectorDataStore):
        if isinstance(store, ROOT.RooTreeDataStore):
            dataset.ConvertToVectorStore()
        else:
            variables = store.get()
            store_name = store.GetName()
            tmp_store = ROOT.RooVectorDataStore(store, variables, store_name)

    array_info = store.getArrays()
    n = array_info.size
    
    # using numpy structed array
    data = np.zeros(n, dtype={'names': (var_lst), 'formats':('f8', 'f8', (n ,len(var_lst)))})

    for x in array_info.reals:
        if x.name in var_lst:
             data[x.name] = np.frombuffer(x.data, dtype = np.float64, count = n)

    for x in array_info.cats:
        if x.name in var_lst:
             data[x.name] = np.frombuffer(x.data, dtype = np.int32, count = n)
    #print(data)
    return data

def DS_to_Numpy(dataset, var_lst):
    # check if root version < 6.27.1
    if ROOT.gROOT.GetVersionInt() < 62701:
        DS_to_Numpy_for_old_version(dataset, var_lst)
    else:
        DS_to_Numpy_for_new_version(dataset, var_lst)
