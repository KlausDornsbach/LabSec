def encode(plain_text, a, b):
    # we ignore characters wich are not alpha using str.isalpha()
    # we treat lower and UPPER case the same way
    try:
        print("aaa")
        coprime_test(26, a)
    except ValueError as e:
        print("Error: a and m must be coprime.")
        raise e
    cache = [None] * 26 # stores cyphers alredy made
    text = plain_text.lower()
    ans = "" # answer
    cont = 0 # how many characters were inserted
    for i in range(0, len(text)):
        if text[i].isdigit():
            ans += text[i]
            cont  += 1
            if cont % 5 == 0:
                ans += " " # formatting (space after 5 char rule)
        if not text[i].isalpha():
            continue # jump over unnecessary
        index = ord(text[i]) - 97   # convert text[i] to ascii integer and subtract 'a' to know index
        if cache[index] != None:  # if it's not a miss
            ans = ans + cache[index]
        else:  #cache miss, calculate
            cypher = (a*index + b) % 26
            aux = chr(cypher + 97)
            cache[index] = aux  # store value
            ans += aux
        cont  += 1
        if cont % 5 == 0:
            ans += " " # formatting (space after 5 char rule)
    return ans.strip()  # if sneaky space is bothering the end of my string

def decode(ciphered_text, a, b):
    if not coprime_test(26, a):
        return 1
    cache = [None] * 26 # stores cyphers alredy discovered
    text = ciphered_text.lower()
    text = text.split()
    text = "".join(text)
    ans = "" # answer
    for i in range(0, len(text)):
        if text[i].isdigit():
            ans += text[i]
            continue
        if not text[i].isalpha():
            continue # jump over unnecessary
        index = ord(text[i]) - 97
        if cache[index] != None:  # if it's not a miss
            ans = ans + cache[index]
        else:  #cache miss, calculate
            mmi = None
            for i in range(1, 26):  # MMI must be in this range
                aux = (i * a) % 26
                if (aux == 1):
                    mmi = i
            decryption = mmi * (index - b) % 26
            aux = chr(decryption + 97)
            cache[index] = aux  # store value
            ans += aux
    return ans
                    
def coprime_test(m, a):
    lowLimit = a
    other = m
    if (m < lowLimit):
        lowLimit = m
        other = a
    for i in range(2, lowLimit//2):
        if a % i == 0 and m % i == 0:
            print("failed")
            raise ValueError("sorry, not coprime")
           # return False  # not coprime
    if (other % lowLimit == 0):
        print("failed 2")
        raise ValueError("sorry, not coprime")
       # return False  # not coprime
    return True