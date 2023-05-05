#
# Pylint Tutorial
#

class car:
    def __init__(self,color):
        self.color =color

my_car = car('blue')

def     crash(car1 ,car2) :
        car1.color= 'burnt'

crash(car('red'),my_car)
print("TESTE")