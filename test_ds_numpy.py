import ROOT

from get_ds       import get_ds
from new_delclones    import delclones
from cuts import cuts_7pi
from DS_to_Numpy import DS_to_Numpy, DS_to_Numpy_for_old_version, DS_to_Numpy_for_new_version
import time

# Создаем переменные RooRealVar
x = ROOT.RooRealVar("x", "x", 0, 10)
y = ROOT.RooRealVar("y", "y", 0, 10)

# Создаем RooDataSet
data = ROOT.RooDataSet("data", "data", ROOT.RooArgSet(x, y))

# Заполняем датасет случайными данными
random_generator = ROOT.TRandom3(42)  # устанавливаем seed
for _ in range(1000):
    x_val = random_generator.Uniform(0, 10)
    y_val = random_generator.Uniform(0, 10)
    x.setVal(x_val)
    y.setVal(y_val)
    data.add(ROOT.RooArgSet(x, y))

ds = data.makeWeighted('x+y')

#ws = DS_to_Numpy_for_new_version(ds, ['x', 'WW', 'W'], True)

ws = DS_to_Numpy_for_new_version(ds, ['x', 'x'], False)
