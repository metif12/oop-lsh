import glob
from lsh import LSH

if __name__ == '__main__' :
  docs = []
  for filename in glob.glob('files/*'):
    with open(filename) as file:
      docs.append(file.read())

  # consider words as shingles
  lsh = LSH(3, 25, docs, True)
  
  # lsh.print_matrix()
  lsh.print_signature()
  lsh.show_similarity()
        
  for comb in lsh.combinations():
    sim = lsh.similarity(comb)
    if sim > 0.35:
      print(comb,sim)
