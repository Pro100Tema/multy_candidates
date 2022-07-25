from ROOT import *
import random as rd
import numpy as np 

run = RooRealVar("run", "run", 0., 10000.)
event = RooRealVar("evt", "evt", 0., 10000.)
x3 = RooRealVar("x3", "x3", 0., 5.)
x4 = RooRealVar("x4", "x4", 0., 10.)
x5 = RooRealVar("x5", "x5", 0., 10.)
x6 =  RooRealVar("x6", "x6", 0., 100000.)
x7 =  RooRealVar("x7", "x7", 0., 100000.)
x8 =  RooRealVar("x8", "x8", 0., 100000.)
x9 =  RooRealVar("x9", "x9", 0., 100000.)
mB = RooRealVar("mB", "mB", 6.15, 6.45)

varset = RooArgSet(run, event, x3, x4, x5, x6, x7, x8, x9, mB)

dataset = ROOT.RooDataSet("dataset", "dataset", varset)

nEvents = 50

for evt in range(nEvents):
    '''
    if evt > 4 and evt % 5 == 0:
        #print(dataset[evt-1].mM)
        rnd_mB = rd.uniform(6.15, 6.45)
        run.setVal(dataset[evt-1].run)
        event.setVal(dataset[evt-1].evt)
        mB.setVal(rnd_mB)
        dataset.add(varset)
    else:
'''
    #rnd_del = rd.randint(5,10)
    if evt > 0 and evt % 5 == 0:
        rnd_num = rd.randint(2,4)
        #dataset[evt-1] * rnd_num
        for i in range(1, rnd_num):
            #dataset.add(dataset[evt - 1])
            rnd_mB = rd.uniform(6.15, 6.45)
            rnd_x3 = rd.uniform(0., 5.)
            rnd_x4 = rd.uniform(0., 10.)
            rnd_x5 = rd.uniform(0., 10.)
            rnd_x6 = rd.uniform(0., 100000.)
            rnd_x7 = rd.uniform(0., 100000.)
            rnd_x8 = rd.uniform(0., 100000.)
            rnd_x9 = rd.uniform(0., 100000.)
            run.setVal(dataset[evt-1].run)
            event.setVal(dataset[evt-1].evt)
            mB.setVal(rnd_mB)
            x3.setVal(rnd_x3)
            x4.setVal(rnd_x4)
            x5.setVal(rnd_x5)
            x6.setVal(rnd_x6)
            x7.setVal(rnd_x7)
            x8.setVal(rnd_x8)
            x9.setVal(rnd_x9)
            dataset.add(varset)
    else:
        rnd_run = rd.randint(0., 1000.)
        rnd_event = rd.randint(0., 1000.)
        rnd_mB = rd.uniform(6.15, 6.45)
        rnd_x3 = rd.uniform(0., 5.)
        rnd_x4 = rd.uniform(0., 10.)
        rnd_x5 = rd.uniform(0., 10.)
        rnd_x6 = rd.uniform(0., 100000.)
        rnd_x7 = rd.uniform(0., 100000.)
        rnd_x8 = rd.uniform(0., 100000.)
        rnd_x9 = rd.uniform(0., 100000.)
        run.setVal(rnd_run)
        event.setVal(rnd_event)
        mB.setVal(rnd_mB)
        x3.setVal(rnd_x3)
        x4.setVal(rnd_x4)
        x5.setVal(rnd_x5)
        x6.setVal(rnd_x6)
        x7.setVal(rnd_x7)
        x8.setVal(rnd_x8)
        x9.setVal(rnd_x9)
        dataset.add(varset)

dataset.SaveAs('example_any_dubles_50.root')

#for i in dataset:
#    print(i.run, i.evt, i.mB)
