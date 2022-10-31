class Ex:
  def __init__(self, num):
    self.num = num

  def __eq__(self, other):
    print('hfgd')
    return self.num == other

x = Ex(1)
print(x.num == 1)