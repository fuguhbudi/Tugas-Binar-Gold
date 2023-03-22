def handle_bad_lines(line):
     panjang_list = len(line)
     if panjang_list == int(28):
        print("masuk lebih besar dari 13")
     if panjang_list == int(27):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]+line[8]+line[9]+line[10]+line[11]+line[12]+line[13]+line[14]
            line.pop(14)
            line.pop(13)
            line.pop(12)
            line.pop(11)
            line.pop(10)
            line.pop(9)
            line.pop(8)
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(26):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]+line[8]+line[9]+line[10]+line[11]+line[12]+line[13]
            line.pop(13)
            line.pop(12)
            line.pop(11)
            line.pop(10)
            line.pop(9)
            line.pop(8)
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(25):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]+line[8]+line[9]+line[10]+line[11]+line[12]
            line.pop(12)
            line.pop(11)
            line.pop(10)
            line.pop(9)
            line.pop(8)
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(24):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]+line[8]+line[9]+line[10]+line[11]
            line.pop(11)
            line.pop(10)
            line.pop(9)
            line.pop(8)
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(23):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]+line[8]+line[9]+line[10]
            line.pop(10)
            line.pop(9)
            line.pop(8)
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(22):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]+line[8]+line[9]
            line.pop(9)
            line.pop(8)
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(21):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]+line[8]
            line.pop(8)
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(20):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]+line[7]
            line.pop(7)
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(19):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]+line[6]
            line.pop(6)
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(18):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]+line[5]
            line.pop(5)
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(17):
            line[0] = line[0]+line[1]+line[2]+line[3]+line[4]
            line.pop(4)
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(16):
            line[0] = line[0]+line[1]+line[2]+line[3]
            line.pop(3)
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(15):
            line[0] = line[0]+line[1]+line[2]
            line.pop(2)
            line.pop(1)
     elif panjang_list == int(14):
            line[0] = line[0]+line[1]
            line.pop(1)
     return line