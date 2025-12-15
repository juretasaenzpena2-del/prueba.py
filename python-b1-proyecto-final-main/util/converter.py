from abc import ABC, abstractmethod
#Write your code here

class Converter(ABC):
  @abstractmethod
  def convert(self,dataFrame,*args) -> list:
      pass  
  def print(self, objects):
    for item in objects:
      print(item.describe())

class CashierConverter(Converter):
  def convert(self,dataFrame):    
    #Write your code here
    pass

class CustomerConverter(Converter):
  #Write your code here
  pass

class ProductConverter(Converter):
  #Write your code here
  pass