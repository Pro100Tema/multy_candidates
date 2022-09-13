import ROOT 
import numpy as np

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
    array_info = store.getBatches(0, n)
    vars = dataset.get()

    if not isinstance(store, ROOT.RooVectorDataStore):
        dataset.ConvertToVectorStore()

    # using numpy structed array
    data = np.zeros(n, dtype={'names': (var_lst), 'formats':('f8', 'f8', (n ,len(var_lst)))})

    count = 0
    for x in array_info:
        if vars[count].GetName() in var_lst:
             data[vars[count].GetName()] = x.second
        count = count + 1
    return data


def DS_to_Numpy(dataset, var_lst):

    store = dataset.store()
    array_info = store.getArrays()
    n = array_info.size

    if not isinstance(store, ROOT.RooVectorDataStore):
        dataset.ConvertToVectorStore()

    # using numpy structed array
    data = np.zeros(n, dtype={'names': (var_lst), 'formats':('f8', 'f8', (n ,len(var_lst)))})

    for x in array_info.reals:
        if x.name in var_lst:
             data[x.name] = np.frombuffer(x.data, dtype = np.float64, count = n)

    for x in array_info.cats:
        if x.name in var_lst:
             data[x.name] = np.frombuffer(x.data, dtype = np.int32, count = n)
                
    return data
