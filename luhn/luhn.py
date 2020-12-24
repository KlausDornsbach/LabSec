class Luhn:
    def __init__(self, card_num):
        string = card_num.split()
        self.card_num = "".join(string) # don't store white space in string
    

    def valid(self):
        string = self.card_num
        if len(string) <= 1:
            #include error: not big enough
            return False

        

        cont = 0    # how many iterations
        total = 0
        for i in range(len(string) - 1,-1, -1):  # first loop: validates string and doubles the %2 == 0 positions
            cont += 1
            
            if (not string[i].isdigit()):
                return False
                #include error: not a digit
            number = int(string[i])          # convert to decimal
            if (cont % 2 == 0):
                number += number
                if (number > 9):
                    number -= 9
            total += number
        if total % 10 == 0:
            return True
        else:
            return False
            #include error: not %10 == 0

