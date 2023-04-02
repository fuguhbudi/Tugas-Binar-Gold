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
                                        HS_Strong,
                                        Kalimat_Alay,
                                        Kalimat_Abusive) 
                                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
                                HS_Strong BOOLEAN,
                                Kalimat_Alay TEXT,
                                Kalimat_Abusive TEXT
                                )
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
             

