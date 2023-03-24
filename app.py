import re
import pandas as pd
import csv
import sqlite3
import emoji as em

from fungsi.handle_baris import handle_bad_lines # import fungsi
from fungsi.connection import connection # import database connection
from fungsi.query import insert_tweet_content, delete_tweet_content, create_tweet_content # import query tweet_content
from fungsi.query import insert_tweet_abusive, delete_tweet_abusive, create_tweet_abusive # import query tweet_abusive
from fungsi.query import insert_tweet_alay, delete_tweet_alay, create_tweet_alay # import query tweet_alay
from fungsi.regex import html_tag, tanda_baca, non_latin_regex, karakter_khusus_regex, kuote_belakang, emoji_regex

from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
app = Flask(__name__)


app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.3.1'),
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


# 0. Remove kalimat Abusive dan Alay menggunakan file inputan

@swag_from("docs/text_processing_file_abusive_dan_alay.yml", methods=['POST'])
@app.route('/text-processing-file-abusive-dan-alay', methods=['POST'])
def text_processing_abusive_and_alay_file():

    conn = connection()
    sql = conn.cursor()

    # Membuat tabel tweet abusive jika belum ada
    sql.execute(create_tweet_content)

    # file = request.files.getlist('file')
    for file in request.files.getlist('file'):
     filename = file.filename
    #  print(file)
    cleaned_text = []
    cleaned_text2 = []
    my_dict = {}
    baris = 0

    # membaca file yang di input. di handle disini adalah
    # - delimeter : sebagai pemisah baris
    # - on_bad_lines : jika di tengah text ada huruf koma di handle oleh fungsi ini (kalo gak ada ini gak bisa dapet semua data)
    # - engine : untuk merubah engine menjadi paython dikarenakan untuk pemrosesan bad lines
    # - header : menandakan baris 1 adalah header jadi tidak diproses
    # - quoting : menghendle text yang memiliki quote di depan dan belakang
    # - encoding : digunakan untuk encoding file yang di input

    data_tweet = pd.read_csv(file, delimiter=',', on_bad_lines=handle_bad_lines, engine='python', header=0, quoting=csv.QUOTE_NONE, encoding='iso-8859-1')
    data_tweet = data_tweet.apply(lambda x: x.str.strip('"') if x.dtype == "object" else x)

    text_tweet = data_tweet["Tweet"] # ambil field tweet

    # buka file kamus kata abusive
    kamus_abusive = pd.read_csv("csv/abusive.csv")
    
    #kamus kata alay
    
    kata_abusive = kamus_abusive["ABUSIVE"] # ambil field abusive

    
    with open('csv/new_kamusalay.csv', 'r') as file_kamus_alay:
     reader = csv.reader(file_kamus_alay)
     for row in reader:
      key = row[0]  # mengambil nilai dari row 0 sebagai kunci
      value = row[1]  # mengambil nilai dari row 1 sebagai nilai
      my_dict[key] = value  # memasukkan data ke dalam kamus
    
     new_dict = {key.replace(',', '='): value.replace(',', ':') for key, value in my_dict.items()}
    
    # agar data tidak bertumpuk di delete semua table kemudian di insert baru bisa di hapus agar semua data masuk
    conn.execute(delete_tweet_content)
    conn.commit()



    # kumpulan function regex yang di gunakan
    # html_tag = re.compile('<.*?>|&nbsp;|&amp;|&lt;|&gt;') # menghapus html tag
    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    hapus_abusive = "|".join(map(re.escape, list(kata_abusive))) # menghapus kata abusive berdasarkan kamus abusive
    # tanda_baca = re.compile(r'(\W)\1+|[@#$%^&;]') # menghapus tanda baca lebih dari satu
    # non_latin_regex = re.compile(r'[^\x00-\x7F]+') # menghapus huruf latin yang tidak terbaca
    # karakter_khusus_regex = re.compile(r'[@$%^&;]') # menghabus karakter kusus
    # kuote_belakang = re.compile(r"\'$") # single quote di belakang
    # emoji_regex = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF]")
    
    combined_pattern = f"{karakter_khusus_regex}|{hapus_abusive}|{html_tag}"

    text_contoh = "USER Ya dkk \xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84'"
    encoded = text_contoh.encode('utf-8')

    # decoded = encoded.decode('unicode_escape')

    emoji = text_contoh.encode('latin1').decode('utf8')

    baris = 0

    text = '\xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84 This is a sample text with emojis \xf0\x9f\x92\xa9\xf0\x9f\x98\x8d\xf0\x9f\x98\xb1'
    text = text.encode('latin1').decode('utf8')
    pattern_emo = '[\U0001F600-\U0001F64F\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+'
    clean_text = re.sub(pattern_emo, '', text)
    # print(clean_text)

    # looping untuk mengganti kata abusive dan dimasukan ke variable cleaned_text dan meng ignore case sensitive dan insert ke database
    # for text in text_tweet:
    for index, text in enumerate(text_tweet):
        cleaned_text2 = tanda_baca.sub(r'\1', re.subn(combined_pattern, '', non_latin_regex.sub('', kuote_belakang.sub('', pattern_alay.sub(lambda m: new_dict[m.group().lower()], text))), flags=re.IGNORECASE)[0])
        # cleaned_text2 = tanda_baca.sub(r'\1', re.sub(combined_pattern, '', non_latin_regex.sub('', kuote_belakang.sub('', text)), flags=re.IGNORECASE))
        # print(cleaned_text2)

        # Tanda koma pada akhir untuk menandakan membuat sebuah tuple dengan satu elemen, 
        # karena jika tidak diberikan tanda koma maka dianggap sebagai tipe data string biasa, bukan tuple.
        sql.execute(insert_tweet_content, ( cleaned_text2,
                                            data_tweet["HS"][index].item(), 
                                            data_tweet["Abusive"][index].item(), 
                                            data_tweet["HS_Individual"][index].item(), 
                                            data_tweet["HS_Group"][index].item(), 
                                            data_tweet["HS_Religion"][index].item(), 
                                            data_tweet["HS_Race"][index].item(), 
                                            data_tweet["HS_Physical"][index].item(), 
                                            data_tweet["HS_Gender"][index].item(), 
                                            data_tweet["HS_Other"][index].item(), 
                                            data_tweet["HS_Weak"][index].item(), 
                                            data_tweet["HS_Moderate"][index].item(), 
                                            data_tweet["HS_Strong"][index].item())
                                            )
        baris=baris+1
        print("{} baris terproses".format(baris)) # untuk debug baris terprocess di terminal karena data banyak dan processnya lama
        cleaned_text.append(re.sub(combined_pattern,r'', text, flags=re.IGNORECASE))

    # Menutup koneksi ke database
    conn.commit()
    conn.close()

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

    response_data = jsonify(json_response)
    return response_data


# 1. Remove kalimat Abusive menggunakan file inputan

@swag_from("docs/text_processing_file_abusive.yml", methods=['POST'])
@app.route('/text-processing-file-abusive', methods=['POST'])
def text_processing_abusive_file():

    conn = connection()
    sql = conn.cursor()

    # Membuat tabel tweet abusive jika belum ada
    sql.execute(create_tweet_abusive)

    # file = request.files.getlist('file')
    for file in request.files.getlist('file'):
     filename = file.filename
    #  print(file)
    cleaned_text = []
    cleaned_text2 = []

    # membaca file yang di input. di handle disini adalah
    # - delimeter : sebagai pemisah baris
    # - on_bad_lines : jika di tengah text ada huruf koma di handle oleh fungsi ini (kalo gak ada ini gak bisa dapet semua data)
    # - engine : untuk merubah engine menjadi paython dikarenakan untuk pemrosesan bad lines
    # - header : menandakan baris 1 adalah header jadi tidak diproses
    # - quoting : menghendle text yang memiliki quote di depan dan belakang
    # - encoding : digunakan untuk encoding file yang di input

    data_tweet = pd.read_csv(file, delimiter=',', on_bad_lines=handle_bad_lines, engine='python', header=0, quoting=csv.QUOTE_NONE, encoding='iso-8859-1')
    data_tweet = data_tweet.apply(lambda x: x.str.strip('"') if x.dtype == "object" else x)

    # buka file kamus kata abusive.csv
    kamus_abusive = pd.read_csv("csv/abusive.csv")

    text_tweet = data_tweet["Tweet"] # ambil field tweet
    kata_abusive = kamus_abusive["ABUSIVE"] # ambil field abusive

    # agar data tidak bertumpuk di delete semua table kemudian di insert baru bisa di hapus gar semua data masuk
    conn.execute(delete_tweet_abusive)
    conn.commit()

    # kumpulan function regex yang di gunakan
    # html_tag = re.compile('<.*?>|&nbsp;|&amp;|&lt;|&gt;') # menghapus html tag
    hapus_abusive = "|".join(map(re.escape, list(kata_abusive))) # menghapus kata abusive berdasarkan kamus abusive
    # tanda_baca = re.compile(r'(\W)\1+|[@#$%^&;]') # menghapus tanda baca lebih dari satu
    # non_latin_regex = re.compile(r'[^\x00-\x7F]+') # menghapus huruf latin yang tidak terbaca
    # karakter_khusus_regex = re.compile(r'[@$%^&;]') # menghabus karakter kusus
    # kuote_belakang = re.compile(r"\'$") # single quote di belakang
    # emoji_regex = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF]")
    
    combined_pattern = f"{karakter_khusus_regex}|{hapus_abusive}|{html_tag}"

    text_contoh = "USER Ya dkk \xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84'"
    encoded = text_contoh.encode('utf-8')

    # decoded = encoded.decode('unicode_escape')

    emoji = text_contoh.encode('latin1').decode('utf8')

    baris = 0

    text = '\xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84 This is a sample text with emojis \xf0\x9f\x92\xa9\xf0\x9f\x98\x8d\xf0\x9f\x98\xb1'
    text = text.encode('latin1').decode('utf8')
    pattern_emo = '[\U0001F600-\U0001F64F\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+'
    clean_text = re.sub(pattern_emo, '', text)
    # print(clean_text)

    # looping untuk mengganti kata abusive dan dimasukan ke variable cleaned_text dan meng ignore case sensitive dan insert ke database
    # for text in text_tweet:
    for index, text in enumerate(text_tweet):
        cleaned_text2 = tanda_baca.sub(r'\1', re.sub(combined_pattern, '', non_latin_regex.sub('', kuote_belakang.sub('', text)), flags=re.IGNORECASE))
        # print(cleaned_text2)

        # Tanda koma pada akhir untuk menandakan membuat sebuah tuple dengan satu elemen, 
        # karena jika tidak diberikan tanda koma maka dianggap sebagai tipe data string biasa, bukan tuple.
        sql.execute(insert_tweet_abusive, ( cleaned_text2,
                                            data_tweet["HS"][index].item(), 
                                            data_tweet["Abusive"][index].item(), 
                                            data_tweet["HS_Individual"][index].item(), 
                                            data_tweet["HS_Group"][index].item(), 
                                            data_tweet["HS_Religion"][index].item(), 
                                            data_tweet["HS_Race"][index].item(), 
                                            data_tweet["HS_Physical"][index].item(), 
                                            data_tweet["HS_Gender"][index].item(), 
                                            data_tweet["HS_Other"][index].item(), 
                                            data_tweet["HS_Weak"][index].item(), 
                                            data_tweet["HS_Moderate"][index].item(), 
                                            data_tweet["HS_Strong"][index].item())
                                            )
        baris=baris+1
        print("{} baris terproses".format(baris)) # untuk debug baris terprocess di terminal karena data banyak dan processnya lama
        cleaned_text.append(re.sub(combined_pattern,r'', text, flags=re.IGNORECASE))

    # Menutup koneksi ke database
    conn.commit()
    conn.close()

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

    response_data = jsonify(json_response)
    return response_data


# 2. remove bahasa Alay menggunakan file inputan

@swag_from("docs/text_processing_file_bahasa_alay.yml", methods=['POST'])
@app.route('/text-processing-file-alay', methods=['POST'])
def text_processing_alay_file():

    conn = connection()
    sql = conn.cursor()
    # Membuat tabel tweet abusive jika belum ada
    sql.execute(create_tweet_alay)

    # Upladed file
    # file = request.files.getlist('file')
    for file in request.files.getlist('file'):
     filename = file.filename

    my_dict = {}
    new_tweet = {}
    new_dict = {}
    # my_tweet = []

    data_tweet = pd.read_csv(file, delimiter=',', on_bad_lines=handle_bad_lines, engine='python', header=0, quoting=csv.QUOTE_NONE, encoding='iso-8859-1')
    # for row_tweet in data_tweet["Tweet"]:
    #  my_tweet.append(row_tweet)
    text_tweet = data_tweet["Tweet"]
    # buka file kamus alay
    with open('csv/new_kamusalay.csv', 'r') as file_kamus_alay:
     reader = csv.reader(file_kamus_alay)
     
     for row in reader:
      key = row[0]  # mengambil nilai dari row 0 sebagai kunci
      value = row[1]  # mengambil nilai dari row 1 sebagai nilai
      my_dict[key] = value  # memasukkan data ke dalam kamus
    
    new_dict = {key.replace(',', '='): value.replace(',', ':') for key, value in my_dict.items()}

    baris = 0

    # kumpulan function regex yang di gunakan
    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    # html_tag = re.compile('<.*?>|&nbsp;|&amp;|&lt;|&gt;') # menghapus html tag
    # tanda_baca = re.compile(r'(\W)\1+|[@#$%^&;]') # menghapus tanda baca lebih dari satu
    # non_latin_regex = re.compile(r'[^\x00-\x7F]+') # menghapus huruf latin yang tidak terbaca
    # karakter_khusus_regex = re.compile(r'[@$%^&;]') # menghabus karakter kusus
    # kuote_belakang = re.compile(r"\'$") # single quote di belakang
    
    combined_pattern = f"{karakter_khusus_regex}|{html_tag}"

    # agar data tidak bertumpuk di delete semua table kemudian di insert baru bisa di hapus gar semua data masuk
    conn.execute(delete_tweet_alay)
    conn.commit()
    
    # Mengganti kata alay dalam setiap kalimat dengan kata yang sesuai dalam kamus_alay menggunakan re.sub
    
    # Disini harus di optimasi lagi karena masih terlalu lama
    # for index in range(len(my_tweet)):
    for index, text in enumerate(text_tweet):
     new_tweet = tanda_baca.sub(r'\1', re.subn(combined_pattern, '', non_latin_regex.sub('', kuote_belakang.sub('', pattern_alay.sub(lambda m: new_dict[m.group().lower()], text))), flags=re.IGNORECASE)[0])



    #  new_tweet[index] = pattern_alay.sub(lambda m: new_dict[m.group().lower()], my_tweet[index])
    #  sql.execute(insert_tweet_alay, (new_tweet[index],))
     sql.execute(insert_tweet_alay, ( new_tweet,
                                         data_tweet["HS"][index].item(), 
                                         data_tweet["Abusive"][index].item(), 
                                         data_tweet["HS_Individual"][index].item(), 
                                         data_tweet["HS_Group"][index].item(), 
                                         data_tweet["HS_Religion"][index].item(), 
                                         data_tweet["HS_Race"][index].item(), 
                                         data_tweet["HS_Physical"][index].item(), 
                                         data_tweet["HS_Gender"][index].item(), 
                                         data_tweet["HS_Other"][index].item(), 
                                         data_tweet["HS_Weak"][index].item(), 
                                         data_tweet["HS_Moderate"][index].item(), 
                                         data_tweet["HS_Strong"][index].item())
                                            )
     baris=baris+1
     print("{} baris terproses".format(baris)) # untuk debug baris terprocess di terminal karena data banyak dan processnya lama

    conn.commit()
    conn.close()

    # my_list = [[s] for s in new_tweet.values()]
    # with open('dataKamusAlay.csv', 'w', newline='') as file:
    #  writer = csv.writer(file)
    #  writer.writerows(my_list)

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

def __init__(self):
        self.conn = sqlite3.connect('database/dbtweet.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
        self.conn.commit()


# 5. Get bahasa Alay yang menggunakan text inputan

@swag_from("docs/text_processing_text_bahasa_alay_get.yml", methods=['GET'])
@app.route('/text-processing-text-alay-get', methods=['GET'])
def text_processing_alay_input_get():

    # koneksikan database dbtweet
    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    sql.execute("SELECT * FROM tweet_alay_text order by id desc")

    # sql.execute(query, (cleaned_text,))
    data = sql.fetchall()


    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': data,
    }

    response_data = jsonify(json_response)
    return response_data


# 6. Get bahasa Abusive yang menggunakan text inputan

@swag_from("docs/text_processing_text_bahasa_abusive_get.yml", methods=['GET'])
@app.route('/text-processing-text-abusive-get', methods=['GET'])
def text_processing_abusive_input_get():

    # koneksikan database dbtweet
    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    sql.execute("SELECT * FROM tweet_abusive_text order by id desc")

    # sql.execute(query, (cleaned_text,))
    data = sql.fetchall()


    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': data,
    }

    response_data = jsonify(json_response)
    return response_data





# 7. Get bahasa Alay yang menggunakan text inputan

@swag_from("docs/text_processing_text_bahasa_alay_get_input.yml", methods=['GET'])
@app.route('/text-processing-text-alay-get-input', methods=['GET'])
def text_processing_alay_input_get_input():

    # koneksikan database dbtweet
    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    sql.execute("SELECT * FROM tweet_alay")

    # sql.execute(query, (cleaned_text,))
    data = sql.fetchall()


    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': data,
    }

    response_data = jsonify(json_response)
    return response_data


# 8. Get bahasa Abusive yang menggunakan text inputan

@swag_from("docs/text_processing_text_bahasa_abusive_get_input.yml", methods=['GET'])
@app.route('/text-processing-text-abusive-get-input', methods=['GET'])
def text_processing_abusive_input_get_input():

    # koneksikan database dbtweet
    connection = sqlite3.connect('database/dbtweet.db')
    sql = connection.cursor()
    sql.execute("SELECT * FROM tweet_abusive")

    # sql.execute(query, (cleaned_text,))
    data = sql.fetchall()


    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': data,
    }

    response_data = jsonify(json_response)
    return response_data



if __name__ == '__main__':
   app.run()

