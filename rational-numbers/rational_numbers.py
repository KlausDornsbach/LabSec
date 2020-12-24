import math

class Rational:
    def __init__(self, numer, denom):
        self.numer = numer
        self.denom = denom
        self.reduce_number()

    def __add__(self, o):
        retorno = Rational(self.numer * o.denom + o.numer * self.denom, self.denom * o.denom)
        retorno.reduce_number()
        return retorno

    def __sub__(self, o):
        retorno = Rational(self.numer * o.denom - o.numer * self.denom, self.denom * o.denom)
        retorno.reduce_number()
        return retorno

    def __mul__(self, o):
        retorno = Rational(self.numer * o.numer, self.denom * o.denom)
        retorno.reduce_number()
        return retorno

    def __truediv__(self, o):
        retorno = Rational(self.numer * o.denom, self.denom * o.numer)
        retorno.reduce_number()
        return retorno
    
    def __abs__(self):
        retorno = Rational(abs(self.numer), abs(self.denom))
        retorno.reduce_number()
        return retorno

    def __pow__(self, o): # rational to real
        if o == 0:
            retorno = Rational(1,1)
        elif o > 0:
            retorno = Rational(self.numer**o, self.denom**o)
        elif o < 0:
            retorno = Rational(self.denom**o, self.numer**o)
        retorno.reduce_number()
        return retorno
        
    def __rpow__(self, o):
        #return self.__pow__(o)
        if o == 0:
            return 0
        if self.numer < 0:
            retorno = pow(o, self.numer) # o**(self.numer/self.denom)
            retorno = pow(retorno, 1.0/self.denom)
        else:
            retorno = pow(o, self.numer) # o**(self.numer/self.denom)
            retorno = pow(retorno, 1.0/self.denom)
        return retorno
        
    def __eq__(self, o):
        if (self.numer == o.numer and self.denom == o.denom):
            return True
        return False
        
    def reduce_number(self):
        if self.numer == self.denom:
            self.denom = 1
            self.numer = 1
        
        if self.numer == 0:
            self.denom = 1
        
        if self.numer * self.denom < 0:
            self.numer = - abs(self.numer)
            self.denom = abs(self.denom)

        if self.numer * self.denom > 0:
            self.numer = abs(self.numer)
            self.denom = abs(self.denom)
        
        lowLimit = abs(self.denom)
        if (abs(self.numer) > lowLimit):
            lowLimit = abs(self.numer)
        for i in range(2, lowLimit):
            if (self.numer % i == 0 and self.denom % i == 0):
                self.numer = self.numer / i
                self.denom = self.denom / i
