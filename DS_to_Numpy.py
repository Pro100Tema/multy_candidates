import ROOT 
import numpy as np

# input: 
# dataset - initial dataset
# var_lst - name of variables to add in numpy array 
#ds = DS_to_Numpy(data, ['evt', 'run'])
# output: 
# data - numpy array with values of the required variables

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

    return data
