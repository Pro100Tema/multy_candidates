# ============================================================================= 
from   __future__        import print_function
# ============================================================================= 
import ostap.fitting.roofit 
import ostap.fitting.models    as     Models 
from   ostap.core.core         import Ostap
import ostap.io.zipshelve      as     DBASE
import ostap.logger.table      as     T 
from   ostap.utils.timing      import timing
from   ostap.utils.utils       import wait
from   ostap.plotting.canvas   import use_canvas
from   ostap.fitting.variables import SETVAR 
from   ostap.utils.utils       import vrange 
from   builtins                import range
import ROOT, time
from ds_to_numpy import ds_to_numpy, ds_to_numpy_for_mid_version, ds_to_numpy_for_old_version, ds_to_numpy_new_version
# =============================================================================
# logging 
# =============================================================================
from ostap.logger.logger import getLogger
if '__main__' == __name__  or '__builtin__' == __name__ : 
    logger = getLogger ( 'test_ds_to_numpy' )
else : 
    logger = getLogger ( __name__ )
# =============================================================================

def test_small_ds():
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

    ws = ds_to_numpy(data, ['x', 'y'], False)
    print(ws)


def test_small_ds_with_weights():
    # Создаем переменные RooRealVar
    x = ROOT.RooRealVar("x", "x", 0, 10)
    y = ROOT.RooRealVar("y", "y", 0, 10)

    # Создаем RooDataSet
    data = ROOT.RooDataSet("data", "data", ROOT.RooArgSet(x, y))

    # Заполняем датасет случайными данными
    random_generator = ROOT.TRandom3(42)  # устанавливаем seed
    for _ in range(60):
        x_val = random_generator.Uniform(0, 10)
        y_val = random_generator.Uniform(0, 10)
        x.setVal(x_val)
        y.setVal(y_val)
        data.add(ROOT.RooArgSet(x, y))

    ds = data.makeWeighted('x+y')
    ws = ds_to_numpy(ds, ['x', 'y', 'W'], True)
    print(ws)


def test_ds_with_weights():
    # Создаем переменные RooRealVar
    x = ROOT.RooRealVar("x", "x", 0, 10)
    y = ROOT.RooRealVar("y", "y", 0, 10)
    z = ROOT.RooRealVar("z", "z", 0, 10)
    q = ROOT.RooRealVar("q", "q", 0, 10)

    # Создаем RooDataSet
    data = ROOT.RooDataSet("data", "data", ROOT.RooArgSet(x, y, z,q))

    # Заполняем датасет случайными данными
    random_generator = ROOT.TRandom3(42)  # устанавливаем seed
    for _ in range(1000):
        x_val = random_generator.Uniform(0, 10)
        y_val = random_generator.Uniform(0, 10)
        z_val = random_generator.Uniform(0, 10)
        q_val = random_generator.Uniform(0, 10)
        x.setVal(x_val)
        y.setVal(y_val)
        z.setVal(z_val)
        q.setVal(q_val)
        data.add(ROOT.RooArgSet(x, y, z, q))

    ds = data.makeWeighted('x+y')

    ws = ds_to_numpy(ds, ['x', 'y', 'W'], True)
    print(ws)
    #ws = ds_to_numpy(ds, ['x', 'x'], False)


def test_large_ds_with_weights():

    # Создаем RooDataSet
    variables = []
    for i in range(100):
        var_name = "x{}".format(i)
        var = ROOT.RooRealVar(var_name, var_name, 0, 10)
        variables.append(var)

    data = ROOT.RooDataSet("data", "data", ROOT.RooArgSet(*variables))

    # Заполняем датасет случайными данными
    random_generator = ROOT.TRandom3(42)  # устанавливаем seed
    for _ in range(1000):
        values = [random_generator.Uniform(0, 10) for _ in range(100)]
        for i, var in enumerate(variables):
            var.setVal(values[i])
        data.add(ROOT.RooArgSet(*variables))

    ds = data.makeWeighted('x1+x2')

    var_lst = ['x2', 'x3','x4', 'x5', 'x6','x7', 'x8', 'x9','x10', 'x1', 'x12','x13', 'x14', 'x15','x16', 'x17', 'x18','x19', 'x20', 'x21','x22', 'x23', 'x24','x25', 'x26', 'x27','x28', 'x29', 'x30','x31', 'x32', 'x33',
               'x34', 'x35', 'x36','x37', 'x38', 'x39','x40', 'x41', 'x42','x43', 'x44', 'x45','x46', 'x47', 'x48','x49', 'x50', 'x51','x52', 'x53', 'x54','x55', 'x56', 'x57','x58', 'x59', 'x60']
    ws = ds_to_numpy(ds, var_lst, False)
    print(ws)
    #ws2 = ds_to_numpy(ds, var_lst, True)

def test_large_ds_without_weights():

    # Создаем RooDataSet
    variables = []
    for i in range(100):
        var_name = "x{}".format(i)
        var = ROOT.RooRealVar(var_name, var_name, 0, 10)
        variables.append(var)

    data = ROOT.RooDataSet("data", "data", ROOT.RooArgSet(*variables))

    # Заполняем датасет случайными данными
    random_generator = ROOT.TRandom3(42)  # устанавливаем seed
    for _ in range(1000):
        values = [random_generator.Uniform(0, 10) for _ in range(100)]
        for i, var in enumerate(variables):
            var.setVal(values[i])
        data.add(ROOT.RooArgSet(*variables))

    var_lst = ['x2', 'x3','x4', 'x5', 'x6','x7', 'x8', 'x9','x10', 'x1', 'x12','x13', 'x14', 'x15','x16', 'x17', 'x18','x19', 'x20', 'x21','x22', 'x23', 'x24','x25', 'x26', 'x27','x28', 'x29', 'x30','x31', 'x32', 'x33',
               'x34', 'x35', 'x36','x37', 'x38', 'x39','x40', 'x41', 'x42','x43', 'x44', 'x45','x46', 'x47', 'x48','x49', 'x50', 'x51','x52', 'x53', 'x54','x55', 'x56', 'x57','x58', 'x59', 'x60']
    
    ws = ds_to_numpy(data, var_lst, False)
    print(ws)


if '__main__' == __name__ :

    with timing ('Test small ds' , logger ) :
        test_small_ds()

    with timing ('Test small ds with weights' , logger ) :
        test_small_ds_with_weights()

    with timing ('Test ds with weights', logger ) :
        test_ds_with_weights()
        
    with timing ('Test large ds with weights', logger ) :
        test_large_ds_with_weights()
    
    with timing ('Test large ds without weights', logger ) :
        test_large_ds_without_weights()
