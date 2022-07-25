import ROOT, glob, os, sys, math
import ostap.fitting.models as Models
import ostap.plotting.canvas as Canvas
from ostap.core.pyrouts import *
from ostap.plotting.style import *
from ostap.plotting.fit_draw import *
from ostap.fitting.basic import PDF

from get_ds       import get_ds
from new_delclones    import delclones
from cuts import cuts_7pi
import time

#data = get_ds('data_rd_7pi.root')

#ds = data.reduce(cuts_7pi)

f = ROOT.TFile('example_50_cand.root', 'read')
ds = f['dataset']
f.close()

'''
h1 = ROOT.TH1F('mB', '', 50, 6.15, 6.45)
ds.project(h1, 'mB')
#h1.red()
#h1.draw('e1')
print("mean before ", h1.mean())
print("rms before  ", h1.rms())
'''
start = time.time()
#ds = delclones(ds, [6.15, 6.45, 'mB'], ['run', 'evt'], 'first')
ds = delclones(ds, ['run', 'evt'], 'first')
done = time.time() - start
print("time delclones ", done)
'''
h2 = ROOT.TH1F('mB', '', 50, 6.15, 6.45)
ds.project(h2, 'mB')
#h2.blue()
#h2.draw('e1 same')
print("mean after ", h2.mean())
print("rms after ", h2.rms())

mb = ds.mB; mb.setMin(6.15); mb.setMax(6.45)
CB2  = Models.CB2_pdf('S'                         ,
                      xvar   = mb                   ,
                      mean   =(6.275, 6.26, 6.28)  , 
                      sigma  = 0.008265361474469714 * 1.010455839744903,
                      alphaR = 1.9644247438756715,
                      alphaL = 1.6645089301687104,
                      nR = 1.947053904313234,
                      nL = 0.4397432050505651
)


bkg = Models.PolyPos_pdf('b', xvar = mb, power = 1)

model = Models.Fit1D(signal = CB2, background = bkg, suffix = '_Bc')
r,f = model.fitTo(ds, draw = True, nbins = 30, refit = True, ncpu = 8) 
print (r)
print(r.S_Bc)
print(model.wilks2('S_Bc', ds, ['mean_S', 'sigma_S']))

model.sPlot(ds)
'''
