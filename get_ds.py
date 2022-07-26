import ROOT

def get_ds ( file_path , verbose = True , key = '') :
  f = ROOT.TFile ( file_path , "read" )
  list_keys = f.GetListOfKeys()
  counter , names = 0 , []
  if verbose : print ('\n# file content:')
  for li in list_keys :
    counter += 1
    if verbose : print ('# {}'.format(str(li.GetName())))
    names.append ( li.GetName() )
  key_ds , nkeys_ds = '' , 0
  for n in names :
    if (n[0:2] == 'ds') or ( key != '' and key in n ):
      key_ds = n ; nkeys_ds += 1
  if nkeys_ds < 1 :
    print ("There's smth wrong with the file with DataSet!") #; exit()
  ds = f.Get ( key_ds ).Clone()
  f.Close()
  if verbose : print ('\n')
  return ds
