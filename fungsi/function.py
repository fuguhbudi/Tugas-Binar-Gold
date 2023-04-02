# mencari kata alay untuk di insert ketable
# ini ikin lama process tapi buat dapat kata alaynya bisa di simpan ke db
def cari_alay(match,jumlah_alay):
       kata = match.group(0)
       jumlah_alay.append(kata)
       return kata

# ini ikin lama process tapi buat dapat kata abusivenya bisa di simpan ke db
# mencari kata abusive untuk di insert ketable
def cari_abusive(match,jumlah_abusive):
       kata = match.group(0)
       jumlah_abusive.append(kata)
       return kata

# digunakan jika encodenya adalah ISO 8859-1
# function untuk handle ketika menemukan baris yang bermasalah atau ada , (koma) di tengah text
# koding sementara masih jelek dan akan di perbaiki
def handle_bad_lines(line):
     panjang_list = len(line)
     if panjang_list == int(27):
            line[0] = ','.join(line[0:14])
            del line[14:0:-1]
     elif panjang_list == int(26):
            line[0] = ','.join(line[0:13])
            del line[13:0:-1]
     elif panjang_list == int(25):
            line[0] = ','.join(line[0:12])
            del line[12:0:-1]
     elif panjang_list == int(24):
            line[0] = ','.join(line[0:11])
            del line[11:0:-1]
     elif panjang_list == int(23):
            line[0] = ','.join(line[0:10])
            del line[10:0:-1]
     elif panjang_list == int(22):
            line[0] = ','.join(line[0:9])
            del line[9:0:-1]
     elif panjang_list == int(21):
            line[0] = ','.join(line[0:8])
            del line[8:0:-1]
     elif panjang_list == int(20):
            line[0] = ','.join(line[0:7])
            del line[7:0:-1]
     elif panjang_list == int(19):
            line[0] = ','.join(line[0:6])
            del line[6:0:-1]
     elif panjang_list == int(18):
            line[0] = ','.join(line[0:5])
            del line[5:0:-1]
     elif panjang_list == int(17):
            line[0] = ','.join(line[0:4])
            del line[4:0:-1]
     elif panjang_list == int(16):
            line[0] = ','.join(line[0:3])
            del line[3:0:-1]
     elif panjang_list == int(15):
            line[0] = ', '.join(line[0:2])
            del line[2:0:-1]
     elif panjang_list == int(14):
            line[0] = line[0]+line[1]
            line.pop(1)
     return line
