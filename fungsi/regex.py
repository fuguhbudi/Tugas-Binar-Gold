import re

# kumpulan function regex yang di gunakan

html_tag = re.compile('<.*?>|&nbsp;|&amp;|&lt;|&gt;') # menghapus html tag
tanda_baca = re.compile(r'(\W)\1+|[@#$%^&;.,!"]') # menghapus tanda baca lebih dari satu
non_latin_regex = re.compile(r'[^\x00-\x7F]+') # menghapus huruf latin yang tidak terbaca
karakter_khusus_regex = re.compile(r'[@$%^&;]') # menghabus karakter kusus
kuote_belakang = re.compile(r"\'$") # single quote di belakang
emoji_regex = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF]")
whitespace_regex = re.compile(r"\s+") # menghapus white space
alphanumeric_regex = re.compile(r'^\w+$') #menghapus alpanumeric
lowercase_regex = re.compile(r'[A-Z]') # mengganti huruf besar
enter_regex = re.compile(r'\n') # menghapus enter atau \n
retweet_regex = re.compile(r'rt')  # menghapus retweet symbol

