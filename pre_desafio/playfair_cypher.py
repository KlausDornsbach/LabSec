class PlayfairCypher:
    
    def __init__(self):
        self.table_key = []

    def format_text(self, text):
        formatted_text = text.split()
        formatted_text = "".join(formatted_text)
        formatted_text = formatted_text.upper()
        return formatted_text

    def digraph_text(self, text):
        out = self.format_text(text)
        length = len(out)
        for i in range(0, length-1, 2):
            if out[i] == out[i+1]:
                out = out[:i+1] + "X" + out[i+1:]
        length = len(out)
        if length % 2 != 0:
            out = out + "X"
        return out

    def create_dictionary(self, key):
        # clean key
        clean_key = self.format_text(key)
        length = len(clean_key)
        
        table_dic = {} # maps: letter -> numerical position
        cont = 0 # counts how many letters were added
        ji = False # monitors if there is already a J or I on dictionary

        # key
        for i in range(length):
            if ji and (clean_key[i] == "J" or clean_key[i] == "I"):
                continue
            if clean_key[i] not in table_dic:
                if clean_key[i] == "J" or clean_key[i] == "I":
                    ji = True
                table_dic[clean_key[i]] = cont
                cont += 1

        # rest of "abc"
        if (ji):
            for i in range(65, 73): # range of upper characters in ascii
                var = chr(i) # gets char
                if var not in table_dic:
                    table_dic[var] = cont
                    cont += 1
            for i in range(75, 91): # range of upper characters in ascii
                var = chr(i)
                if var not in table_dic:
                    table_dic[var] = cont
                    cont += 1
        else:
            for i in range(65, 91): # range of upper characters in ascii
                var = chr(i) # gets char
                if (var == "J"):
                    continue
                if var not in table_dic:
                    table_dic[var] = cont
                    cont += 1

        return table_dic

    def create_default_matrix(self):
        table = [[0 for x in range(5)] for y in range(5)]
        for i in range(25):
            table[i//5][i%5] = "X"
        return table

    def stringfy_matrix(self, matrix):
        out = ""
        for i in range(len(matrix[0])):
            for j in range(len(matrix)):
                out += matrix[i][j] + " "
            out += "\n"
        return out

    def create_table_key(self, key):
        dictionary = self.create_dictionary(key)
        return self.create_matrix(dictionary)

    def create_matrix(self, dictionary):
        table = [[0 for x in range(5)] for y in range(5)]
        for i in dictionary: # create key matrix
            table[dictionary[i]//5][dictionary[i]%5] = i
        return table

    def decypher(self, matrix, cyphered_text):
        formatted_text = self.digraph_text(cyphered_text)
        out = ""
        i1, j1, i2, j2 = -1, -1, -1, -1
        found = False
        for k in range(0, len(formatted_text), 2):
            # search for letters in matrix
            for i in range(5):
                for j in range(5):
                    if matrix[i][j] == formatted_text[k]:
                        i1 = i
                        j1 = j
                        if i2 != -1:
                            found = True
                            break
                    if matrix[i][j] == formatted_text[k+1]:
                        i2 = i
                        j2 = j
                        if i1 != -1:
                            found = True
                            break
                if found:
                    break
            # test case
            if j1 == j2:
                out += matrix[(i1-1)%5][j1] + matrix[(i2-1)%5][j2] + " " 
            elif i1 == i2:
                out += matrix[i1][(j1-1)%5] + matrix[i2][(j2-1)%5] + " "
            else:
                out += matrix[i1][(j2)] + matrix[i2][(j1)] + " "
            i1, j1, i2, j2 = -1, -1, -1, -1
            found = False
        return out
                    
    def cypher(self, matrix, plain_text):
        formatted_text = self.digraph_text(plain_text)
        out = ""                                            #! output
        i1, j1, i2, j2 = -1, -1, -1, -1                     #! letter positions 
        found = False                                       #! stops iterator when both letters found
        for k in range(0, len(formatted_text), 2):          # iterates text
            # search for letters in matrix
            for i in range(5):                              # iterates lines key-matrix
                for j in range(5):                          # iter. col. key=matrix
                    if matrix[i][j] == formatted_text[k]:   # compares text to matrix
                        i1 = i                              # armazenate variable
                        j1 = j
                        if i2 != -1:                        # if other letter was already found,
                            found = True                    # sets variable to true
                            break                           # jumps out of iteration
                    if matrix[i][j] == formatted_text[k+1]: # ^ same as the last one ^
                        i2 = i
                        j2 = j
                        if i1 != -1:
                            found = True
                            break
                if found:
                    break
            # test case
            if j1 == j2:                                    # if letters of digraph on same column 
                out += matrix[(i1+1)%5][j1] + matrix[(i2+1)%5][j2] + " " 
            elif i1 == i2:                                  # if letters of digraph on same line
                out += matrix[i1][(j1+1)%5] + matrix[i2][(j2+1)%5] + " "
            else:                                           # if all else fails 
                out += matrix[i1][(j2)] + matrix[i2][(j1)] + " "
            i1, j1, i2, j2 = -1, -1, -1, -1                 # resets variables
            found = False                                   # ^ same ^
        return out