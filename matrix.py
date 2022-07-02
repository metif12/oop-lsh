from ipaddress import collapse_addresses


class Matrix:
  def __init__(self, num_rows, num_cols, default):
    self.num_rows = num_rows
    self.num_cols = num_cols
    self.data = [[default for j in range(num_cols)] for i in range(num_rows)]

  def addrow(self, row):
    self.data.append(row)

  def setrow(self, i, row):
    self.data[i] = row

  def getrow(self, i):
    return self.data[i]

  def addcol(self, col):
    for row in self.data:
      row.append(col.pop())

  def addcol(self, j, col):
    for row in self.data:
      row[j] = col.pop()

  def getcol(self, j):
    col = []
    for row in self.data:
      col.append(row[j])
      
    return col

  def setcell(self, i, j, v):
    self.data[i][j] = v

  def getcell(self, i, j):
    return self.data[i][j]

  def col_first_one_idx(self, j):
    for i in range(self.num_rows):
      if self.data[i][j] == 1:
        return i
  
  def __str__(self):
    lines = []
    for i in range(self.num_rows):
      row = map(str, self.getrow(i))
      rowstr = ', '.join(row)
      lines.append(f'{i}: {rowstr}')
      
    return '\n'.join(lines)
