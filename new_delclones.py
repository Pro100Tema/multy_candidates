import sys
import random as rd
import ROOT
import numpy as np

# this function takes index list of multy values and returns one index depending on the sort parametr
# index_lst - index list of multy events
# sort_param - parameter for removimg multy candidates
def analyse(index_lst, sort_param):
    if (len(index_lst) == 1):
        return int(index_lst[0])
    if (sort_param == 'first'):
        return int(index_lst[0])
    if (sort_param == 'last'):
        return int(index_lst[-1])
    if (sort_param == 'random'):
        rnd_index = np.random.choice(len(index_lst), size=1, replace=False)
        return int(index_lst[rnd_index])

def delclones(dataset, compare_lst, sort_param):   
    ds_without_clone=dataset.Clone()
 
    # (run, event) list values
    check_lst = np.array([])

    # index list of multy events
    index_lst = np.array([])

    analyse_index_lst = np.array([[1,2]])
    
    N = len(dataset)
    ds_without_clone.reset()

    # find user variables in dataset
    argset = dataset.get()
    runvar = argset.find(compare_lst[0])
    evtvar = argset.find(compare_lst[1])

    #for i in dataset:
    #    print(i.run, i.evt, i.mB)
    #print('\n')

    # check - no entries in dataset
    if (len(dataset) == 0):
        print("Dataset is empty")
        exit()

    # check correct sort parametr
    if not(sort_param in ('first', 'last', 'random')):
        print("Incorrect sort parametr value")
        exit()

    # fill 2D array from dataset
    for i in range(0, N):
        analyse_index_lst = np.insert(analyse_index_lst, i, (runvar.getValue(dataset[i]), evtvar.getValue(dataset[i])), axis = 0)
    analyse_index_lst = np.delete(analyse_index_lst, -1, axis = 0)

    
    # split 2D array into 2 categories: unique and non-unique
    uniq, uniq_idx, counts = np.unique(analyse_index_lst, axis=0, return_index=True, return_counts=True)
    uniq_lst = uniq[counts == 1]
    non_uniq_lst = uniq[counts > 1]
    
    # split array index 2 categories: unique and non-unique 
    array_idx = np.arange(analyse_index_lst.shape[0]) # the indices of array
    nuniq_idx = array_idx[np.in1d(array_idx, uniq_idx[counts==1], invert=True)]
    uniq_idx = np.delete(array_idx, nuniq_idx)
    #print(nuniq_idx)

    print ('\n Found ', str(len(uniq_idx)), ' non-repeatable events')
    print ('\n Found ', str(len(nuniq_idx)), ' repeatable events')

    # loop to remove multy candidates and select one candidates, according user option
    for i in range(0, len(nuniq_idx) - 1):
        if (i == len(nuniq_idx)-1):
            j = i
        else:
            j = i + 1
            
        if not((runvar.getValue(dataset[int(nuniq_idx[i])]), evtvar.getValue(dataset[int(nuniq_idx[i])])) in check_lst):
            check_lst = np.append(check_lst,((runvar.getValue(dataset[int(nuniq_idx[i])]), evtvar.getValue(dataset[int(nuniq_idx[i])]))))
            index_lst = np.append(index_lst, int(nuniq_idx[i]))

        if(runvar.getValue(dataset[int(nuniq_idx[i])]) == runvar.getValue(dataset[int(nuniq_idx[j])]) and evtvar.getValue(dataset[int(nuniq_idx[i])]) == evtvar.getValue(dataset[int(nuniq_idx[j])])):
            index_lst = np.append(index_lst, int(nuniq_idx[j]))
            if(i == len(nuniq_idx)-2):
              k = analyse(index_lst, sort_param)
              uniq_idx = np.append(uniq_idx, k)  
        else:
            k = analyse(index_lst, sort_param)
            uniq_idx = np.append(uniq_idx, k)
            index_lst = np.array([])
            mass_lst = np.array([])
    
    uniq_idx.sort()

    for i in uniq_idx:
        ds_without_clone.add(dataset[int(i)])

    print ('\n Found ', str(len(ds_without_clone)), ' unique events')
    print ('\n Found ', str(len(dataset) - len(ds_without_clone)), ' dublicates')

    #for i in ds_without_clone:
    #    print(i.run, i.evt, i.mB)
    return ds_without_clone
