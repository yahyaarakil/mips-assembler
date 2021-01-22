def toBinary(numberString, length):
    def flip(c): 
        return '1' if (c == '0') else '0'
    if int (numberString) < 0:
        bin = ('{0:b}'.format(int(numberString)).zfill(length)).replace('-', '')
        n = len(bin)  
        ones = "" 
        twos = "" 
        # for ones complement flip every bit  
        for i in range(n): 
            ones += flip(bin[i])  
    
        # for two's complement go from right  
        # to left in ones complement and if 
        # we get 1 make, we make them 0 and  
        # keep going left when we get first  
        # 0, make that 1 and go out of loop  
        ones = list(ones.strip("")) 
        twos = list(ones) 
        for i in range(n - 1, -1, -1): 
        
            if (ones[i] == '1'): 
                twos[i] = '0'
            else:          
                twos[i] = '1'
                break
    
        i -= 1    
        # If No break : all are 1 as in 111 or 11111  
        # in such case, add extra 1 at beginning  
        if (i == -1): 
            twos.insert(0, '1')
        return "1"*(length-len(twos))+"".join(twos)
    return '{0:b}'.format(int(numberString)).zfill(length)

print("toBinary(5, 5):    " + str(toBinary(5, 5)))
print("toBinary(-5, 5):   " + str(toBinary(-5, 5)))
print("toBinary(\"5\", 5):  " + str(toBinary("5", 5)))
print("toBinary(\"-5\", 5): " + str(toBinary("-5", 5)))