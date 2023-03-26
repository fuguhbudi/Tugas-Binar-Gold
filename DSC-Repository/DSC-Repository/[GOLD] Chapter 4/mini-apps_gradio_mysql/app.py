import mysql.connector
import pandas as pd
import gradio as gr

# koneksi ke server local database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="classicmodels"
)

# query buat baca data dari tabel
cursor = conn.cursor()
cursor.execute("""SELECT * FROM customers 
                WHERE country = 'USA'
                """)
result = cursor.fetchall()

# buat list dari hasil query
fetchData = list(result)

# buat fungsi untuk menampilkan list di Gradio
def getData():
    # cek apakah list kosong
    if not fetchData:
        return "Tidak ada data yang ditemukan"
    else:
        # buat DataFrame pandas dari list
        df = pd.DataFrame(fetchData, columns=[i[0] for i in cursor.description])
        return df

# buat Gradio interface
ui = gr.Interface(fn=getData, 
                     inputs=None,
                     title="Data Customers", 
                     outputs=["dataframe"])

# run Gradio interface
ui.launch()