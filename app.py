import re
import pandas as pd
import csv
import sqlite3


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


# 1. Remove kalimat Abusive menggunakan file inputan

@swag_from("docs/text_processing_file_abusive.yml", methods=['POST'])
@app.route('/text-processing-file-abusive', methods=['POST'])
def text_processing_abusive_file():
    # koneksikan database dbtweet
    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    # Membuat tabel tweet abusive jika belum ada
    sql.execute('''
    CREATE TABLE IF NOT EXISTS tweet_abusive (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        tweet TEXT
        )
    ''')

    for file in request.files.getlist('file'):
     filename = file.filename

    cleaned_text = []
    cleaned_text2 = []

    # function untuk handle ketika menemukan baris yang bermasalah atau ada , (koma) di tengah text
    def handle_bad_lines(line):
     line[0] = line[0]+line[1]+line[2]
     return line

    # membaca file yang di input. di handle disini adalah
    # - delimeter : sebagai pemisah baris
    # - on_bad_lines : jika di tengah text ada huruf koma di handle oleh fungsi ini
    # - engine : untuk merubah engine menjadi paython dikarenakan untuk pemrosesan bad lines
    # - header : menandakan baris 1 adalah header jadi tidak diproses
    # - quoting : menghendle text yang memiliki quote di depan dan belakang
    # - encoding : digunakan untuk encoding file yang di input
    data_tweet = pd.read_csv(file, delimiter=',', on_bad_lines=handle_bad_lines, engine='python', header=0, quoting=csv.QUOTE_NONE, encoding='iso-8859-1')
    
    # buka file kamus kata abusive.csv
    kamus_abusive = pd.read_csv("csv/abusive.csv")

    text_tweet = data_tweet["Tweet"] # ambil field tweet
    kata_abusive = kamus_abusive["ABUSIVE"] # ambil field abusive

    # digunakan sebagai bahan acuan untuk mereplace  kata abusive
    pattern = "|".join(map(re.escape, list(kata_abusive)))

    # query untuk insert ke table tweet_abusive 
    query = "INSERT INTO tweet_abusive (tweet) VALUES (?)"
    
    # looping untuk mengganti kata abusive dan dimasukan ke variable cleaned_text dan meng ignore case sensitive dan insert ke database
    for text in text_tweet:
        cleaned_text2 = re.sub(pattern,r'', text, flags=re.IGNORECASE)
        #Tanda koma pada akhir untuk menandakan membuat sebuah tuple dengan satu elemen, karena jika tidak diberikan tanda koma maka dianggap sebagai tipe data string biasa, bukan tuple.
        sql.execute(query, (cleaned_text2,))
        cleaned_text.append(re.sub(pattern,r'', text, flags=re.IGNORECASE))

    connection.commit()
    connection.close()

    # cetak ke file dataKamusAbusive.csv buat output atau pengecekan aja
    my_list = [[s] for s in cleaned_text]
    with open('dataKamusAbusive.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerows(my_list)

    # output Swagger
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    # Menutup koneksi ke database
    connection.close()
    
    response_data = jsonify(json_response)
    return response_data


# 2. remove bahasa Alay menggunakan file inputan

@swag_from("docs/text_processing_file_bahasa_alay.yml", methods=['POST'])
@app.route('/text-processing-file-alay', methods=['POST'])
def text_processing_alay_file():

    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    # Membuat tabel tweet abusive jika belum ada
    sql.execute('''
    CREATE TABLE IF NOT EXISTS tweet_alay (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        tweet TEXT
        )
    ''')

    # Upladed file
    # file = request.files.getlist('file')
    for file in request.files.getlist('file'):
     filename = file.filename
    #  print(filename)
        

    # Import file csv ke Pandas
    # df = pd.read_csv(file)

    # Import file csv ke Pandas sebagai data pembanding regex
    # dfKamusAlay = pd.read_csv("csv/new_kamusalaynewlagi.csv",encoding = "utf-8",low_memory=False, errors='ignore', delim_whitespace = True)
    
    # baca file kamus alay untuk di bandingkan ke data parsingan
    # dfKamusAlay = pd.read_csv("csv/datautf.csv", error_bad_lines=False)
    # dfAbusive = pd.read_csv("csv/abusive.csv")
    # dfaaaaaa = pd.read_csv("csv/new_kamusalay.csv", encoding='iso-8859-1')

    # with open('csv/new_kamusalay.csv', 'r') as file:
    #  reader = csv.reader(file)
    # for row in reader:
    #  print(row)


    my_dict = {}
    new_tweet = {}
    new_dict = {}
    my_tweet = []
    
    # dfaaaaaa = csv.DictReader(dfaaaaaa, delimiter=',')

    def handle_bad_lines(line):
     line[0] = line[0]+line[1]+line[2]
    #  print(line[0])
     return line
    #  return ','.join(parts)


    text_tweet = pd.read_csv(file, delimiter=',', on_bad_lines=handle_bad_lines, engine='python', header=0, quoting=csv.QUOTE_NONE, encoding='iso-8859-1')
    for row_tweet in text_tweet["Tweet"]:
     my_tweet.append(row_tweet)
    
    # buka file kamus alay
    with open('csv/new_kamusalay.csv', 'r') as file_kamus_alay:
     reader = csv.reader(file_kamus_alay)
     
     for row in reader:
      key = row[0]  # mengambil nilai dari row 0 sebagai kunci
      value = row[1]  # mengambil nilai dari row 1 sebagai nilai
      my_dict[key] = value  # memasukkan data ke dalam kamus
    
    new_dict = {key.replace(',', '='): value.replace(',', ':') for key, value in my_dict.items()}

    baris = 0

    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    # pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    # pattern_quotes = re.compile(r'"{3}|"', flags=re.IGNORECASE)
    # combined_pattern = re.compile(f'({pattern_alay.pattern}|{pattern_quotes.pattern})')
        # pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b|"|""', flags=re.IGNORECASE)

    
    # Mengganti kata alay dalam setiap kalimat dengan kata yang sesuai dalam kamus_alay menggunakan re.sub
    query = "INSERT INTO tweet_alay (tweet) VALUES (?)"
    
    # Disini harus di optimasi lagi karena masih terlalu lama
    for index in range(len(my_tweet)):
     new_tweet[index] = pattern_alay.sub(lambda m: new_dict[m.group().lower()], my_tweet[index])
     sql.execute(query, (new_tweet[index],))
     baris=baris+1
     print("{} baris terproses".format(baris)) # untuk pengecekan/liat baris terprocess di terminal karena data banyak dan processnya lama

    connection.commit()
    connection.close()

    my_list = [[s] for s in new_tweet.values()]
    with open('dataKamusAlay.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerows(my_list)

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': new_tweet,
    }
    

    response_data = jsonify(json_response)
    return response_data

# 3. Remove bahasa Abusive menggunakan inputan text

@swag_from("docs/text_processing_text_abusive.yml", methods=['POST'])
@app.route('/text-processing-text-abusive', methods=['POST'])
def text_processing_abusive_input():

   # koneksikan database dbtweet
    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    # Membuat tabel tweet abusive jika belum ada
    sql.execute('''
    CREATE TABLE IF NOT EXISTS tweet_abusive_text (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        tweet TEXT
        )
    ''')

    textAbusive = request.form.get('text')
    cleaned_text = ""

    data_abusive = pd.read_csv("csv/abusive.csv")
    kata_abusive = data_abusive["ABUSIVE"]

    pattern = "|".join(map(re.escape, list(kata_abusive)))

    cleaned_text = re.sub(pattern,r'', textAbusive, flags=re.IGNORECASE)
    query = "INSERT INTO tweet_abusive_text (tweet) VALUES (?)"
    sql.execute(query, (cleaned_text,))


    connection.commit()
    connection.close()

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


# 4. Remove bahasa Alay menggunakan text inputan

@swag_from("docs/text_processing_text_bahasa_alay.yml", methods=['POST'])
@app.route('/text-processing-text-alay', methods=['POST'])
def text_processing_alay_input():

    # koneksikan database dbtweet
    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    # Membuat tabel tweet alay jika belum ada
    sql.execute('''
    CREATE TABLE IF NOT EXISTS tweet_alay_text (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        tweet TEXT
        )
    ''')

    # ambil value input text dari swagger
    text_alay = request.form.get('text')
    
    my_dict = {}
    new_dict = {}
    cleaned_text = ""
    
    # buka file kamus alay format csv kemudian di definisikan ke variable dictionary baru
    with open('csv/new_kamusalay.csv', 'r') as file:
     reader = csv.reader(file)
     for row in reader:
      key = row[0]  # mengambil nilai dari row 0 sebagai kunci
      value = row[1]  # mengambil nilai dari row 1 sebagai nilai
      my_dict[key] = value  # memasukkan data ke dalam kamus
    
    new_dict = {key.replace(',', '='): value.replace(',', ':') for key, value in my_dict.items()}
    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    
    cleaned_text = pattern_alay.sub(lambda m: new_dict[m.group().lower()], text_alay)
    query = "INSERT INTO tweet_alay_text (tweet) VALUES (?)"
    sql.execute(query, (cleaned_text,))


    connection.commit()
    connection.close()

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()
