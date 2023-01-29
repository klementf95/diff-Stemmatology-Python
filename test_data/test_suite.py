# creating the necessary test format for the original perl script
import os

files = os.listdir('./test_data/parzival')
with open('./test_data/parzival-all.txt', 'w') as fh:
  for f in files:
    if f.endswith('.txt'):
      sigil = f.replace('.txt', '')
      with open('./test_data/parzival/' + "%s" % f) as witness:
        line = "%s     %s" % (sigil, witness.read())
        fh.write(line)
        

files = os.listdir('./test_data/heinrichi')
with open('./test_data/heinrichi-all.txt', 'w') as fh:
  for f in files:
    if f.endswith('.txt'):
      sigil = f.replace('.txt', '')
      with open('./test_data/heinrichi/' + "%s" % f, encoding='ISO-8859-15') as witness:
        line = "%s     %s" % (sigil, witness.read())
        fh.write(line)