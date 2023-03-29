# query untuk insert ke table tweet_content 
insert_tweet_content = """INSERT INTO   tweet_content 
                                    (   tweet,
                                        HS, 
                                        Abusive, 
                                        HS_Individual, 
                                        HS_Group, 
                                        HS_Religion, 
                                        HS_Race, 
                                        HS_Physical, 
                                        HS_Gender, 
                                        HS_Other, 
                                        HS_Weak, 
                                        HS_Moderate, 
                                        HS_Strong) 
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """

# Query Delete isi table tweet_content
delete_tweet_content = "DELETE FROM tweet_content"

# Membuat tabel tweet_content jika belum ada
create_tweet_content = """
                            CREATE TABLE IF NOT EXISTS tweet_content (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                tweet TEXT,
                                HS BOOLEAN,
                                Abusive BOOLEAN,
                                HS_Individual BOOLEAN,
                                HS_Group BOOLEAN,
                                HS_Religion BOOLEAN,
                                HS_Race BOOLEAN,
                                HS_Physical BOOLEAN,
                                HS_Gender BOOLEAN,
                                HS_Other BOOLEAN,
                                HS_Weak BOOLEAN,
                                HS_Moderate BOOLEAN,
                                HS_Strong BOOLEAN
                                )
                        """

# query untuk insert ke table tweet_abusive 
insert_tweet_abusive = """INSERT INTO   tweet_abusive 
                                    (   tweet,
                                        HS, 
                                        Abusive, 
                                        HS_Individual, 
                                        HS_Group, 
                                        HS_Religion, 
                                        HS_Race, 
                                        HS_Physical, 
                                        HS_Gender, 
                                        HS_Other, 
                                        HS_Weak, 
                                        HS_Moderate, 
                                        HS_Strong) 
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """

# Query Delete isi table tweet_abusive
delete_tweet_abusive = "DELETE FROM tweet_abusive"

# Membuat tabel tweet abusive jika belum ada
create_tweet_abusive = """
                            CREATE TABLE IF NOT EXISTS tweet_abusive (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                tweet TEXT,
                                HS BOOLEAN,
                                Abusive BOOLEAN,
                                HS_Individual BOOLEAN,
                                HS_Group BOOLEAN,
                                HS_Religion BOOLEAN,
                                HS_Race BOOLEAN,
                                HS_Physical BOOLEAN,
                                HS_Gender BOOLEAN,
                                HS_Other BOOLEAN,
                                HS_Weak BOOLEAN,
                                HS_Moderate BOOLEAN,
                                HS_Strong BOOLEAN
                                )
                        """

# query untuk insert ke table tweet_abusive 
insert_tweet_alay = """INSERT INTO   tweet_alay
                                    (   tweet,
                                        HS, 
                                        Abusive, 
                                        HS_Individual, 
                                        HS_Group, 
                                        HS_Religion, 
                                        HS_Race, 
                                        HS_Physical, 
                                        HS_Gender, 
                                        HS_Other, 
                                        HS_Weak, 
                                        HS_Moderate, 
                                        HS_Strong) 
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """

# Query Delete isi table tweet_abusive
delete_tweet_alay = "DELETE FROM tweet_alay"

# Membuat tabel tweet abusive jika belum ada
create_tweet_alay = """
                            CREATE TABLE IF NOT EXISTS tweet_alay (
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                tweet TEXT,
                                HS BOOLEAN,
                                Abusive BOOLEAN,
                                HS_Individual BOOLEAN,
                                HS_Group BOOLEAN,
                                HS_Religion BOOLEAN,
                                HS_Race BOOLEAN,
                                HS_Physical BOOLEAN,
                                HS_Gender BOOLEAN,
                                HS_Other BOOLEAN,
                                HS_Weak BOOLEAN,
                                HS_Moderate BOOLEAN,
                                HS_Strong BOOLEAN
                                )
                        """

# Query Delete isi table tweet_abusive
delete_kalimat_alay = "DELETE FROM kalimat_alay"

# Membuat tabel dengan kolom yang dibutuhkan
create_table_alay = """
                            CREATE TABLE IF NOT EXISTS kalimat_alay(
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                                kata_alay TEXT, 
                                jumlah int
                                )
                        """

# query untuk insert ke table tweet_abusive 
insert_alay_word = """INSERT INTO kalimat_alay(
                                    kata_alay,
                                    jumlah
                                    )
                             VALUES (?,?)
                        """

# query untuk update ke table tweet_abusive 
update_alay_word = """UPDATE   kalimat_alay
                        SET    jumlah = ?
                        WHERE  kata_alay = ?
                   """

# Membuat tabel dengan kolom yang dibutuhkan
create_table_abusive = """
                            CREATE TABLE IF NOT EXISTS kalimat_abusive(
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                                kata_alay TEXT, 
                                jumlah int
                                )
                    """

# query untuk insert ke table tweet_abusive 
insert_abusive_word =   """INSERT INTO kalimat_abusive(
                                    kata_alay,
                                    jumlah
                                    )
                             VALUES (?,?)
                        """

# query untuk update ke table tweet_abusive 
update_abusive_word =   """UPDATE   kalimat_abusive
                                SET    jumlah = ?
                                WHERE  kata_alay = ?
                        """






# Membuat tabel tweet text jika belum ada
create_tweet_text = """
                CREATE TABLE IF NOT EXISTS tweet_text (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        tweet TEXT
                        )
             """

# query untuk insert ke table tweet text 
insert_tweet_text =   """INSERT INTO tweet_text(
                                    tweet
                                    )
                             VALUES (?)
                        """
             

