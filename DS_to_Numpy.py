import ROOT 
import numpy as np


def DS_to_Numpy(dataset, var_lst):
    store = dataset.store()
    data = {}

    if not isinstance(store, ROOT.RooVectorDataStore):
        dataset.ConvertToVectorStore()

    array_info = store.getArrays()

    for x in array_info.reals:
        if x.name in var_lst:
            data[x.name] = np.frombuffer(x.data, dtype=np.float64, count=array_info.size)
    return data
