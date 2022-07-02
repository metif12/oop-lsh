from itertools import combinations
import random
import re
import matplotlib.pyplot as plt
import numpy as np
from matrix import Matrix

class LSH:
  def __init__(self, k, num_permutes, docs, word = True):
    self.word = word
    self.k = k
    self.num_permutes = num_permutes
    self.docs = docs
    self.doc_shingles = []
    self.shingles = []
    self.matrix = None
    self.signature = None
    self.extract()
    self.build_matrix()
    self.sign()

  def extract_words(self,doc):
    ws = re.sub(r'[^\w\s]', '', doc).lower().split()
    
    for w in ws:
      if w not in self.shingles:
        self.shingles.append(w)
    
    return list(set(ws))
    
  def extract_chars(self,doc):
    ws = []
    i = 0
    while True:
      j = i + self.k
      if j < len(doc):
        w = doc[i:j]        
        ws.append(w)
        if w not in self.shingles:
          self.shingles.append(w)
      else:
        break

      i += 1

    return list(set(ws))
      
  def extract(self):
    for doc in self.docs:
      if self.word:
        ws = self.extract_words(doc)
      else:
        ws = self.extract_chars(doc)
        
      self.doc_shingles.append(ws)

  def build_matrix(self):
    self.matrix = Matrix(len(self.shingles), len(self.docs), 0)

    for j,doc in enumerate(self.doc_shingles):
      for i,shingle in enumerate(self.shingles):
        if shingle in doc:
          self.matrix.setcell(i,j,1)

  def get_permute(self):
    order = [ o for o in range(len(self.shingles))]
    random.shuffle(order)
    return order

  def get_signature(self, permute):
    signed = []
    for j in range(self.matrix.num_cols):
      col = self.matrix.getcol(j)
      for idx in permute:
        if col[idx] == 1:
          signed.append(idx)
          break

    return signed

  def sign(self):
    self.signature = Matrix(self.num_permutes, len(self.docs),0)

    for n in range(self.num_permutes):
      permute = self.get_permute()
      signed = self.get_signature(permute)
      self.signature.setrow(n, signed)

  def similarity(self, combination):
    sum = 0
    for i in range(self.signature.num_rows):
      if self.signature.getcell(i,combination[0]) == self.signature.getcell(i,combination[1]):
        sum += 1

    if sum == 0 :
      return 0

    return float(sum) / self.signature.num_rows
  
  def print_matrix(self):
    print(self.matrix)
      
  def print_signature(self):
    print(self.signature)
    
  def combinations(self):
    combinations = []
    for x in range(len(self.docs)):
      for y in range(x+1, len(self.docs)):
        combinations.append((x,y))
        
    return combinations

  def show_similarity(self):
    height = list()
    bars = set()

    for comb in self.combinations():
      sim = self.similarity(comb)
      height.append(sim)
      bars.add(comb)

    x_pos = np.arange(len(bars))

    # Create bars and choose color
    plt.bar(x_pos, height, color=(0.5, 0.1, 0.5, 0.6))

    # Add title and axis names
    plt.title('Similarity')
    plt.xlabel('Files')
    plt.ylabel('Files')

    # Create names on the x axis
    plt.xticks(x_pos, bars)

    # Show graph
    plt.show()