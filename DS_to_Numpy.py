import ROOT 
import numpy as np
import os

# input: 
# dataset - initial dataset
# var_lst - name of variables to add in numpy array 
# weight - Bool value, which work with weights vars in dataset
#ds = DS_to_Numpy(data, ['evt', 'run'], weight)
#ds = DS_to_Numpy_for_old_version(data, ['evt', 'run']) - for old ROOT package version
# output: 
# data - numpy array with values of the required variables

def add_weight(ds, data, var_lst):
    weight_name = ds.weightVar().GetName()
    if not weight_name in ds:
            weight_array = np.zeros(ds.numEntries(), dtype=np.float64)
            for i in range(ds.numEntries()):
                ds.get(i)
                weight_array[i] = ds.weight()
            if weight_name in var_lst:
                data[weight_name] = weight_array
            else:
                print("No weigths vars in variables list")
                exit()
    return data

def DS_to_Numpy_for_old_version(dataset, var_lst, weight): 
    store = dataset.store()
    n = store.size()
    vars = dataset.get()

    if not isinstance(store, ROOT.RooVectorDataStore):
        if isinstance(store, ROOT.RooTreeDataStore):
            dataset.ConvertToVectorStore()
        else:
            variables = store.get()
            store_name = store.GetName()
            store = ROOT.RooVectorDataStore(store, variables, store_name)
        
    # using numpy structed array
    format = [(name, 'f8') for name in var_lst]
    data = np.zeros(n, dtype= format)
    #data = np.zeros(n, dtype={'names': (var_lst), 'formats':('f8', 'f8', (n ,len(var_lst)))})

    # for large datasets
    # check batch size * var size < 10^6 
    num_entries = store.numEntries()
    count_vars = len(vars)
    data_limit = num_entries * count_vars
    num_limit = 1000000
    remainder = n % num_limit
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
        #print(rargs)
        data_part = []
        for first, num in rargs:
            array_info = store.getBatches(first, num)
            count = 0
            for x in array_info:
                if vars[count].GetName() in var_lst:
                    data_part.append(str(x.second))
                    #print(data_part)
                count = count + 1
        data = np.array(data_part, dtype= object)

        #print(len(data))
        #print(data[0])

    if weight and dataset.isWeighted():
        add_weight(dataset, data, var_lst)

    return data


def DS_to_Numpy_for_new_version(dataset, var_lst, weight):
    store = dataset.store()

    if not isinstance(store, ROOT.RooVectorDataStore):
        if isinstance(store, ROOT.RooTreeDataStore):
            dataset.ConvertToVectorStore()
        else:
            variables = store.get()
            store_name = store.GetName()
            store = ROOT.RooVectorDataStore(store, variables, store_name)

    array_info = store.getArrays()
    n = array_info.size
    
    # using numpy structed array
    format = [(name, 'f8') for name in var_lst]
    data = np.zeros(n, dtype= format)

    for x in array_info.reals:
        if x.name in var_lst:
             data[x.name] = np.frombuffer(x.data, dtype = np.float64, count = n)

    for x in array_info.cats:
        if x.name in var_lst:
             data[x.name] = np.frombuffer(x.data, dtype = np.int32, count = n)
    #print(data)
    if weight and dataset.isWeighted():
        add_weight(dataset, data, var_lst)

    return data

def ds_to_numpy(dataset, var_lst, weight):
    ds_new = dataset.subset(var_lst)
    data = ds_new.to_numpy()

    #create structed array
    dtype_list = [(key, data[key].dtype) for key in data.keys()]
    structured_array = np.array(list(zip(*data.values())), dtype=dtype_list)

    if weight and dataset.isWeighted():
        add_weight(dataset, data, var_lst)

    return structured_array


#def DS_to_Numpy(dataset, var_lst):
#    # check if root version < 6.27.1
#    if ROOT.gROOT.GetVersionInt() < 62701:
#        DS_to_Numpy_for_old_version(dataset, var_lst)
#    else:
#        DS_to_Numpy_for_new_version(dataset, var_lst)

def DS_to_Numpy(dataset, var_lst, weight = False):
    root_version = ROOT.gROOT.GetVersionInt()
    # check if root version < 6.24.0
    if root_version < 62400:
        DS_to_Numpy_for_old_version(dataset, var_lst, weight)
    elif 62400 <= root_version < 62600:
        DS_to_Numpy_for_new_version(dataset, var_lst, weight)
    else:
        ds_to_numpy(dataset, var_lst, weight)
