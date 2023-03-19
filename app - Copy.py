import re
import pandas as pd
import csv


from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

# @swag_from("docs/hello_world.yml", methods=['GET'])
# @app.route('/', methods=['GET'])
# def hello_world():
#     json_response = {
#         'status_code': 200,
#         'description': "Menyapa Hello World",
#         'data': "Hello World",
#     }

#     response_data = jsonify(json_response)
#     return response_data

# @swag_from("docs/text.yml", methods=['GET'])
# @app.route('/text', methods=['GET'])
# def text():
#     json_response = {
#         'status_code': 200,
#         'description': "Original Teks",
#         'data': "Halo, apa kabar semua?",
#     }

#     response_data = jsonify(json_response)
#     return response_data

# @swag_from("docs/text_clean.yml", methods=['GET'])
# @app.route('/text-clean', methods=['GET'])
# def text_clean():
#     json_response = {
#         'status_code': 200,
#         'description': "Teks yang sudah dibersihkan",
#         'data': re.sub(r'[^a-zA-Z0-9]', ' ', "Halo, apa kabar semua?"),
#     }

#     response_data = jsonify(json_response)
#     return response_data

# @swag_from("docs/text_processing.yml", methods=['POST'])
# @app.route('/text-processing', methods=['POST'])
# def text_processing():

#     text = request.form.get('text')

#     json_response = {
#         'status_code': 200,
#         'description': "Teks yang sudah diproses",
#         'data': re.sub(r'[^a-zA-Z0-9]', ' ', text),
#     }

#     response_data = jsonify(json_response)
#     return response_data

#abusive

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file)

    # Import file csv ke Pandas sebagai data pembanding regex
    # dfKamusAlay = pd.read_csv("csv/new_kamusalaynewlagi.csv",encoding = "utf-8",low_memory=False, errors='ignore', delim_whitespace = True)
    
    # baca file kamus alay untuk di bandingkan ke data parsingan
    dfKamusAlay = pd.read_csv("csv/datautf.csv", error_bad_lines=False)
    dfAbusive = pd.read_csv("csv/abusive.csv")
    dfaaaaaa = pd.read_csv("csv/new_kamusalay.csv", encoding='iso-8859-1')

    # with open('csv/new_kamusalay.csv', 'r') as file:
    #  reader = csv.reader(file)
    # for row in reader:
    #  print(row)


    my_dict = {}
    my_tweet = []
    dfaaaaaa = csv.DictReader(dfaaaaaa, delimiter=',')

    with open("csv/datautf2.csv", "r") as fileTweet:
     dfKamusAlay = pd.read_csv("csv/datautf2.csv", error_bad_lines=False)
    #  readerTweet = csv.reader(fileTweet["Tweet"])
     for rowTweet in dfKamusAlay["Tweet"]:
      my_tweet.append(rowTweet)
    
    with open('csv/new_kamusalay.csv', 'r') as file:
     reader = csv.reader(file)
     
     for row in reader:
    #   my_dict.update(row)
    #   my_dict[row[0]] = row[1]
      key = row[0]  # mengambil nilai dari row 0 sebagai kunci
      value = row[1]  # mengambil nilai dari row 1 sebagai nilai
      my_dict[key] = value  # memasukkan data ke dalam kamus
    
    
    new_dict = {}
    
    new_dict = {key.replace(',', '='): value.replace(',', ':') for key, value in my_dict.items()}


    #print(new_dict)
    # Iterasi setiap baris di dalam file CSV
    # for row in dfaaaaaa:
    #  my_dict.update(row)

        # Menambahkan setiap baris ke dalam dictionary my_dict
    #  my_dict[row[1]] = "aaa"


    # print(my_tweet)

    #dfKamusAlay = pd.read_csv(file)
    #textsAlay = dfKamusAlay.text.to_list()

    pattern = dfAbusive["ABUSIVE"]
    pattern2 =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

     #export file menjadi csv
#    dfKamusAlay.to_csv('namafile_export.csv', index=False)

    # Ambil teks yang akan diproses dalam format list
    # texts = dfKamusAlay.text.to_list()
    texts = dfKamusAlay["Tweet"]

    # textsxxxx = pattern.text.to_list()

    cleaned_text2 = []
    # Loop through the alay_dict and replace each alay word with its replacement
    # for key, value in my_dict.items():
    #   #  cleaned_text2.append(re.sub(key, value, str(texts)))
    #     cleaned_text2 = re.sub(key, value, textDb)
    #     print(cleaned_text2)
    # print(my_dict.items())
    # print(my_tweet)
    # for i in range(len(my_tweet)):
    #  for kata, pengganti in  my_dict.items():
    #   my_tweet[i] = my_tweet[i].replace(kata, pengganti)

    # print(my_tweet)
    # print(my_dict.items())

    # Kamus alay
    # alay_dict = {'Gue': 'banget', 'tp': 'tapi', 'yg': 'yang', 'lg': 'lagi'}
    # print(alay_dict)
    # List teks yang akan diubah
    # text_list = ['Gue lg baca buku tp ga ngerti yg dimaksud si penulis bgt.', 'Dia lg maen game lgsg mati tp ga ngerasa kesel yg lgsg restart lg.']
    # text_list = ["- disaat semua cowok berusaha melacak perhatian eug. loe lantas remehkan perhatian yg gue kasih khusus ke elo. basic elo cowok bego ! ! !'", "RT USER: USER siapa yang telat ngasih tau elu?edan sarap gue bergaul dengan cigax jifla calis sama siapa noh licew juga'"]
    # Mengganti kata-kata alay dengan kata-kata standar pada setiap teks dalam list
    # new_list = []
    # for s in my_tweet:
    #     for key, value in new_dict.items():
    #         s = re.sub(r"\b%s\b" % key, value, s)  # Menggunakan regex word boundary \b
    #     new_list.append(s)
    #     print(s)
    # for i in range(len(text_list)):
    #     for alay_word, standard_word in new_dict.items():
    #         text_list[i] = text_list[i].replace(alay_word, standard_word)
    # print(my_tweet)
    # print(new_list)

    # if i in text:
    #     text = text.replace(i, '***REPLACED***')


    # for kalimat in my_tweet:
        # print(kalimat)


    # texts = dfKamusAlay.text.to_list()
    s_tuple = tuple(pattern)
    s_string = str(list(pattern))

    # print(list(pattern))
    # Lakukan cleansing pada teks
    pattern = "|".join(map(re.escape, list(pattern)))

    cleaned_text = []
    for text in texts:
         cleaned_text.append(re.sub(pattern,r'', text, flags=re.IGNORECASE))
        #  new_string = re.sub(pattern, replacement, my_string)  
       #  cleaned_text.append(re.sub(texts, ' ', text))
    # print(cleaned_text)
    # print(my_dict)

    # with open('dataKamusAbusive.csv', mode='w', newline='') as filesssss:
    #  writers = csv.writer(filesssss)
    #  for row in cleaned_text:
    #     writers.writerow(row)

    my_list = [[s] for s in cleaned_text]
    with open('dataKamusAbusive.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerows(my_list)


    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data






#remove bahasa alay

@swag_from("docs/text_processing_file2.yml", methods=['POST'])
@app.route('/text-processing-file2', methods=['POST'])
def text_processing_file2():
    import pprint


    # Upladed file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file)

    # Import file csv ke Pandas sebagai data pembanding regex
    # dfKamusAlay = pd.read_csv("csv/new_kamusalaynewlagi.csv",encoding = "utf-8",low_memory=False, errors='ignore', delim_whitespace = True)
    
    # baca file kamus alay untuk di bandingkan ke data parsingan
    dfKamusAlay = pd.read_csv("csv/datautf.csv", error_bad_lines=False)
    dfAbusive = pd.read_csv("csv/abusive.csv")
    dfaaaaaa = pd.read_csv("csv/new_kamusalay.csv", encoding='iso-8859-1')

    # with open('csv/new_kamusalay.csv', 'r') as file:
    #  reader = csv.reader(file)
    # for row in reader:
    #  print(row)


    my_dict = {}
    my_tweet = []
    dfaaaaaa = csv.DictReader(dfaaaaaa, delimiter=',')

    def handle_bad_lines(line):
     line[0] = line[0]+line[1]+line[2]
     print(line[0])
     return line
    #  return ','.join(parts)


    with open("csv/datautf2.csv", "r") as fileTweet:
    #  dfKamusAlay = pd.read_csv("csv/datautf2.csv", error_bad_lines=False)
     dfKamusAlay = pd.read_csv("csv/datautf2.csv", delimiter=',', on_bad_lines=handle_bad_lines, engine='python', header=0, quoting=csv.QUOTE_NONE)
    #  readerTweet = csv.reader(fileTweet["Tweet"])
     for rowTweet in dfKamusAlay["Tweet"]:
      my_tweet.append(rowTweet)
    
    #  print(my_tweet)
    with open('csv/new_kamusalay.csv', 'r') as file:
     reader = csv.reader(file)
     
     for row in reader:
    #   my_dict.update(row)
    #   my_dict[row[0]] = row[1]
      key = row[0]  # mengambil nilai dari row 0 sebagai kunci
      value = row[1]  # mengambil nilai dari row 1 sebagai nilai
      my_dict[key] = value  # memasukkan data ke dalam kamus
    
    tweet = dfKamusAlay["Tweet"]
    new_dict = {}
    
    new_dict = {key.replace(',', '='): value.replace(',', ':') for key, value in my_dict.items()}


    #print(new_dict)
    # Iterasi setiap baris di dalam file CSV
    # for row in dfaaaaaa:
    #  my_dict.update(row)

        # Menambahkan setiap baris ke dalam dictionary my_dict
    #  my_dict[row[1]] = "aaa"


    # print(my_tweet)

    #dfKamusAlay = pd.read_csv(file)
    #textsAlay = dfKamusAlay.text.to_list()

    pattern = dfAbusive["ABUSIVE"]
    pattern2 =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

     #export file menjadi csv
     #dfKamusAlay.to_csv('namafile_export.csv', index=False)

    # Ambil teks yang akan diproses dalam format list
    # texts = dfKamusAlay.text.to_list()
    texts = dfKamusAlay["Tweet"]

    cleaned_text2 = []

    # Kamus alay
    # alay_dict = {'Gue': 'banget', 'tp': 'tapi', 'yg': 'yang', 'lg': 'lagi'}
    # print(alay_dict)
    # List teks yang akan diubah
    # text_list = ['Gue lg baca buku tp ga ngerti yg dimaksud si penulis bgt.', 'Dia lg maen game lgsg mati tp ga ngerasa kesel yg lgsg restart lg.']
    text_list = ["- disaat semua cowok berusaha melacak perhatian eug. loe lantas remehkan perhatian yg gue kasih khusus ke elo. basic elo cowok bego ! ! !'", "RT USER: USER siapa yang telat ngasih tau elu?edan sarap gue bergaul dengan cigax jifla calis sama siapa noh licew juga'"]
    # Mengganti kata-kata alay dengan kata-kata standar pada setiap teks dalam list


    # new_list = []
    # for s in my_tweet:
    #     for key, value in new_dict.items():
    #         s = re.sub(r"\b%s\b" % key, value, s)  # Menggunakan regex word boundary \b
    #     new_list.append(s)
    #     print(s)


    # Membuat pattern dari kamus_alay

    # Fungsi untuk melakukan penggantian kata alay dalam kalimat
    # def ganti_kata_alay(m):
    #     # return new_dict[m.group()]
    #     if m.group() in new_dict:
    #         return new_dict[m.group()]
    #     else:
    #         return m.group()

    a = 0
    new_tweet = {}

    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    # pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    # pattern_quotes = re.compile(r'"{3}|"', flags=re.IGNORECASE)
    # combined_pattern = re.compile(f'({pattern_alay.pattern}|{pattern_quotes.pattern})')
        # pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b|"|""', flags=re.IGNORECASE)

    # print(my_tweet)
    # Mengganti kata alay dalam setiap kalimat dengan kata yang sesuai dalam kamus_alay menggunakan re.sub
    for i in range(len(my_tweet)):
        # new_tweet[i] = pattern_alay.sub(ganti_kata_alay, my_tweet[i])
        new_tweet[i] = pattern_alay.sub(lambda m: new_dict[m.group().lower()], my_tweet[i])
        a=a+1
        print("{} baris terproses".format(a))


    # print(new_tweet)



    # if i in text:
    #     text = text.replace(i, '***REPLACED***')


    # for kalimat in my_tweet:
        # print(kalimat)

    my_list = [[s] for s in new_tweet.values()]
    with open('dataKamusAlay.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerows(my_list)


    # with open('data.csv', mode='w') as file:
    #  for i in range(len(new_tweet)):
    #   writer = csv.writer(file)
    #   print(new_tweet[i])
    #   writer.writerow(new_tweet[i])


    # writer.writerow(my_tweet)


    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': new_tweet,
    }
    

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()

