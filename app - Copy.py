import re
import pandas as pd
import csv
import sqlite3
import emoji

from fungsi.handle_baris import handle_bad_lines # import fungsi
from fungsi.connection import connection # import database connection
from fungsi.query import insert_tweet_content, delete_tweet_content, create_tweet_content
from fungsi.query import create_tweet_text, insert_tweet_text # import query tweet_abusive
from fungsi.regex import html_tag, tanda_baca, non_latin_regex, karakter_khusus_regex, kuote_belakang, emoji_regex #import fungsi regex
from fungsi.regex import whitespace_regex, enter_regex, alphanumeric_regex, lowercase_regex
# retweet_regex, username_regex
# from fungsi.regex import url_regex, whitespace_regex2

from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
app = Flask(__name__)


app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.4.1'),
    'description': LazyString(lambda: 'Dokumentasi API untuk data processing untuk penghapusan bahasa alay dan abusive menggunakan file inputan dan text'),
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


# 1. Remove kalimat Abusive dan Alay menggunakan file inputan

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
    # data_tweet = pd.read_csv(file, delimiter=',', on_bad_lines=handle_bad_lines, engine='python', header=0, quoting=csv.QUOTE_NONE, encoding='iso-8859-1')

    data_tweet = pd.read_csv(file, encoding='latin-1')


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
    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    hapus_abusive = "|".join(map(re.escape, list(kata_abusive))) # menghapus kata abusive berdasarkan kamus abusive

    # regex yang digunakan untuk processing
    combined_pattern = f"{karakter_khusus_regex}|{html_tag}|{non_latin_regex}|{whitespace_regex}|{alphanumeric_regex}|{hapus_abusive}"

    # looping untuk mengganti kata abusive dan dimasukan ke variable cleaned_text dan meng ignore case sensitive dan insert ke database
    for index, text in enumerate(text_tweet):
        cleaned_text2 = tanda_baca.sub(r'\1', 
                        re.subn( combined_pattern, '',
                        non_latin_regex.sub('', 
                        kuote_belakang.sub('', 
                        pattern_alay.sub(lambda m: new_dict[m.group().lower()], 
                        lowercase_regex.sub(lambda x: x.group(0).lower(), text)))), 
                        flags=re.IGNORECASE)[0])
        
        # pattern_alay.sub(lambda m: new_dict[m.group().lower()], text)
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
        baris=baris+1 #buat debuging saja
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

# 2. Remove bahasa Alay menggunakan text inputan

@swag_from("docs/text_processing_text_bahasa_alay.yml", methods=['POST'])
@app.route('/text-processing-text-alay', methods=['POST'])
def text_processing_alay_input():

    # koneksikan database dbtweet
    conn = connection()
    sql = conn.cursor()

    # Membuat tabel tweet alay jika belum ada
    sql.execute(create_tweet_text)

    # ambil value input text dari swagger
    text_alay = request.form.get('text')
    
    my_dict = {}
    new_dict = {}
    cleaned_text = ""

    # buka file kamus kata abusive
    kamus_abusive = pd.read_csv("csv/abusive.csv")
    
    #kamus kata alay
    kata_abusive = kamus_abusive["ABUSIVE"] # ambil field abusive
    
    # buka file kamus alay format csv kemudian di definisikan ke variable dictionary baru
    with open('csv/new_kamusalay.csv', 'r') as file:
     reader = csv.reader(file)
     for row in reader:
      key = row[0]  # mengambil nilai dari row 0 sebagai kunci
      value = row[1]  # mengambil nilai dari row 1 sebagai nilai
      my_dict[key] = value  # memasukkan data ke dalam kamus
    
    new_dict = {key.replace(',', '='): value.replace(',', ':') for key, value in my_dict.items()}
    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)

    # kumpulan function regex yang di gunakan
    pattern_alay = re.compile(r'\b(' + '|'.join(new_dict.keys()) + r')\b', flags=re.IGNORECASE)
    hapus_abusive = "|".join(map(re.escape, list(kata_abusive))) # menghapus kata abusive berdasarkan kamus abusive
    
    # regex yang digunakan untuk processing
    combined_pattern = f"{karakter_khusus_regex}|{html_tag}|{non_latin_regex}|{whitespace_regex}|{alphanumeric_regex}|{hapus_abusive}"

    # cleaned_text = pattern_alay.sub(lambda m: new_dict[m.group().lower()], text_alay)
    cleaned_text = tanda_baca.sub(r'\1', 
                        re.subn( combined_pattern, '',
                        non_latin_regex.sub('', 
                        kuote_belakang.sub('', 
                        pattern_alay.sub(lambda m: new_dict[m.group().lower()], 
                        lowercase_regex.sub(lambda x: x.group(0).lower(), text_alay)))), 
                        flags=re.IGNORECASE)[0])
    

    sql.execute(insert_tweet_text, (cleaned_text,))


    conn.commit()
    conn.close()

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
   app.run()

