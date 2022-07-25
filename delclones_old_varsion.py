# this function takes the original dataset as input and removes all repeating (multy) candidates inside indicated range
# input: 
# delclones(dataset, range_lst, sort_param):
# dataset - input dataset with clones
# range_lst - min and max value for the range and name of the variable, for example: 6.15, 6.45, mB
# sort_param - parameter for removimg multy candidates, 
#              for example: first cand, last cand, random choise, min value for mass, max value for mass
# the function returns a dataset without repeating events (no multy cand)
# output: 
# return new data_set ds_without_clones
# ========================================================================================================
import sys
import random as rd
import ROOT
import numpy as np

# helper
key = sys.argv[1]
if (key == '-h' or key == '--help'):
    print("Function definition: ds = delclones(dataset, range_lst, sort_par)\n", 
          "dataset - input dataset with clones\n", 
          "range_lst - min and max value for the range and name of the variable, for example: 6.15, 6.45, mB\n", 
          "sort_param - parameter for removimg multy candidates,\n", 
          "for example: first cand, last cand, random choise, min value for mass, max value for mass.\n",
          "For example you can use clone_remove.py file")

# this function takes index list of multy values and returns one index depending on the sort parametr
# index_lst - index list of multy events
# mass_lst - mass list of events
# sort_param - parameter for removimg multy candidates
def analyse(index_lst, mass_lst, sort_param):
    if (len(index_lst) == 1):
        return int(index_lst[0])
    if (sort_param == 'first'):
        return int(index_lst[0])
    if (sort_param == 'last'):
        return int(index_lst[-1])
    if (sort_param == 'random'):
        rnd_index = np.random.choice(len(index_lst), size=1, replace=False)
        return int(index_lst[rnd_index])
    if (sort_param == 'min'):
        min_index = np.argmin(mass_lst)
        return int(index_lst[min_index])
    if (sort_param == 'max'):
        max_index = np.argmax(mass_lst)
        return int(index_lst[max_index])

def delclones(dataset, range_lst, compare_lst, sort_param):   
    ds_without_clone=dataset.Clone()

    # mass list of events
    mass_lst = np.array([])
 
    # (run, event) list values
    check_lst = np.array([])

    # index list of multy events
    index_lst = np.array([])

    #dataset = dataset.reduce(ROOT.RooArgSet(dataset.run, dataset.evt, dataset.mB))
    N = len(dataset)
    print(N)
    ds_without_clone.reset()

    # find user variables in dataset
    argset = dataset.get()
    mvar = argset.find(range_lst[2])
    runvar = argset.find(compare_lst[0])
    evtvar = argset.find(compare_lst[1])

    # check - no entries in dataset
    if (len(dataset) == 0):
        print("Dataset is empty")
        exit()

    # check that range is correct
    if (range_lst[1] < range_lst[0]):
        print("Max value of range less then min value in range")
        exit()

    # check correct sort parametr
    if not(sort_param in ('first', 'last', 'random', 'min', 'max')):
        print("Incorrect sort parametr value")
        exit()
    
    # check that the variable exist in dataset
    if not(range_lst[2] in argset):
        print("This variable is not in the dataset")
        exit()

    # delete event that doesn't fall in the interval
    for ev in dataset:
        if (mvar.getValue() < range_lst[0] or mvar.getValue() > range_lst[1]):
            del ev

    #for i in dataset:
    #    print(i.mB, i.run, i.evt)
    #print('\n')

    # find all multy events and put index in index_lst dataset
    for i in range (0, N-1):
        if (i == N-1):
            j = i
        else:
            j = i + 1
            
        if not((runvar.getValue(dataset[i]), evtvar.getValue(dataset[i])) in check_lst):
            #using numpy library
            check_lst = np.append(check_lst,(runvar.getValue(dataset[i]), evtvar.getValue(dataset[i])))
            index_lst = np.append(index_lst, i)
            mass_lst = np.append(mass_lst, mvar.getValue(dataset[i]))

        if(runvar.getValue(dataset[i]) == runvar.getValue(dataset[j]) and evtvar.getValue(dataset[i]) == evtvar.getValue(dataset[j])):
            index_lst = np.append(index_lst, j)
            mass_lst = np.append(mass_lst, mvar.getValue(dataset[j]))
            if (i == N-2):
                k = analyse(index_lst, mass_lst, sort_param)
                #print(k)
                ds_without_clone.add(dataset[k])
        else:
            k = analyse(index_lst, mass_lst, sort_param)
            #print(k)
            ds_without_clone.add(dataset[k])
            #print(index_lst)
            index_lst = np.array([])
            mass_lst = np.array([])

    #for i in ds_without_clone:
    #    print(i.mB, i.run, i.evt)
    print ('\n\n Found ', str(len(dataset) - len(ds_without_clone)), ' dublicates in range from ', range_lst[0], ' to ', range_lst[1], ' with variable ', range_lst[2])
    return ds_without_clone




'''
    for i in range (0, N - 1):
        index_lst.append(i)
        mass_lst.append(mvar.getValue(dataset[i]))
        for j in range (i + 1, N):
            if(dataset[i].run.ve().value() == dataset[j].run.ve().value() and dataset[i].evt.ve().value() == dataset[j].evt.ve().value()):
                index_lst.append(j)
                mass_lst.append(mvar.getValue(dataset[j]))
        k = analyse(index_lst, mass_lst, sort_param)
        if not((dataset[k].run.ve().value(), dataset[k].evt.ve().value()) in check_lst):
            check_lst.append((dataset[k].run.ve().value(), dataset[k].evt.ve().value()))
            ds_without_clone.add(dataset[k])
        index_lst.clear()
        mass_lst.clear()
    print ('\n\n Found ', str(len(dataset) - len(ds_without_clone)), ' dublicates in range from ', range_lst[0], ' to ', range_lst[1], ' with variable ', range_lst[2])
    return ds_without_clone
'''
