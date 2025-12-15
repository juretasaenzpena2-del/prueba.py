#Write your code here

class FoodPackage (ABC): 
    @abstractmethod
    def pack(self)  -> str:
        pass
    @abstractmethod
    def material(self) -> str:
        pass
    def describe(self):
        return f"Empaque: {self.pack()} , Material: {self.material()}"    
    
class Wrapping(FoodPackage):  
  #Write your code here
  pass

class Bottle(FoodPackage):  
  #Write your code here
  pass
      
class Glass(FoodPackage):  
  #Write your code here
  pass

class Box(FoodPackage):  
  #Write your code here
  pass