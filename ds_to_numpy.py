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

def add_weight(ds, data, weight_var):
    if ds.isWeighted():
        weight_name = ds.weightVar().GetName()
        if not weight_name in ds:
                weight_array = np.zeros(ds.numEntries(), dtype=np.float64)
                for i in range(ds.numEntries()):
                    ds.get(i)
                    weight_array[i] = ds.weight()
                if weight_name in weight_var:
                #    print("+++")
                #    print(weight_name)
                    data[weight_name] = weight_array
                else:
                    print("No weigths vars in weights list")
                    exit()
        else:
            print(f"Field with name '{weight_name}' already exists in the data")
            exit()
    else: 
        print("Dataset is not weighted")
        exit()
    #print(data)
    return data

def ds_to_numpy_for_old_version(dataset, var_lst, weight_var):
    len_ds_vars = dataset.get().getSize()
    # если в списке необходимых переменных меньше, чем в датасете, то сначала делаем маленький датасет и только потом преобразование в numpy массив
    if len(var_lst) < len_ds_vars/2:
        subset_ds = dataset.subset(var_lst)
        store = subset_ds.store()
        n = store.size()
        vars = subset_ds.get()
    else:    
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

    print(vars)
    if data_limit < num_limit:
        array_info = store.getBatches(0, n)
        count = 0
        for x in array_info:
            if count < len(var_lst):
                data[var_lst[count]] = x.second
            count = count + 1
    else: 
        rargs = [(i*num_limit, num_limit) for i in range(nb)] + [(nb * num_limit,r)]
        #print(rargs)
        data_part = []
        for first, num in rargs:
            array_info = store.getBatches(first, num)
            count = 0
            for x in array_info:
                if count < len(var_lst):
                    data_part.append(str(x.second))
                count = count + 1
        data = np.array(data_part, dtype= object)

    if weight_var:
        add_weight(dataset, data, var_lst)

    return data


def ds_to_numpy_for_mid_version(dataset, var_lst, weight_var):

    #количество переменных в начальном датасете
    len_ds_vars = dataset.get().getSize()
    # если в списке необходимых переменных меньше, чем в датасете, то сначала делаем маленький датасет и только потом преобразование в numpy массив
    if len(var_lst) < len_ds_vars/2:
        subset_ds = dataset.subset(var_lst)
        store = subset_ds.store()
    else:    
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
            
    if weight_var:
        add_weight(dataset, data, var_lst)
        
    return data

def ds_to_numpy_new_version(dataset, var_lst, weight_var):
    var_lst2 = var_lst.copy()
    if weight_var and dataset.isWeighted():
        #print("+")
        weight_name = dataset.weightVar().GetName()
        if weight_name in var_lst2:
            var_lst2.remove(weight_name)
        vars_subset = var_lst2.copy()
        #print("subset: ", vars_subset)
        #print("var_lst: ", var_lst)
        ds_new = dataset.subset(vars_subset)
        data = ds_new.to_numpy()
    else:
        ds_new = dataset.subset(var_lst)
        data = ds_new.to_numpy()

    #create structed array
    dtype_list = [(key, data[key].dtype) for key in data.keys()]
    structured_array = np.array(list(zip(*data.values())), dtype=dtype_list)

    if weight_var:
        add_weight(dataset, data, var_lst)

    return structured_array

def ds_to_numpy(dataset, var_lst, weight_var = False):
    root_version = ROOT.gROOT.GetVersionInt()
    # check if root version < 6.24.0
    if root_version < 62400:
        np_array = ds_to_numpy_for_old_version(dataset, var_lst, weight_var)
    elif 62400 <= root_version < 62600:
        np_array = ds_to_numpy_for_mid_version(dataset, var_lst, weight_var)
    else:
        np_array = ds_to_numpy_new_version(dataset, var_lst, weight_var)
    return np_array
