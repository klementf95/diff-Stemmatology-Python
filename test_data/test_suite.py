import os

files = os.listdir('./test_data/parzival')
with open('./test_data/parzival-all.txt', 'w') as fh:
  for f in files:
    if f.endswith('.txt'):
      sigil = f.replace('.txt', '')
      with open('./test_data/parzival/' + "%s" % f) as witness:
        line = "%s     %s" % (sigil, witness.read())
        fh.write(line)
        

files = os.listdir('./test_data/legend')
with open('./test_data/legend-all.txt', 'w') as fh:
  for f in files:
    if f.endswith('.txt'):
      sigil = f.replace('.txt', '')
      with open('./test_data/legend/' + "%s" % f, encoding='ISO-8859-15') as witness:
        line = "%s     %s" % (sigil, witness.read())
        fh.write(line)