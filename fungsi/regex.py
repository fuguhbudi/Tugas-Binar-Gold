import re

# kumpulan function regex yang di gunakan
html_tag = re.compile('<.*?>|&nbsp;|&amp;|&lt;|&gt;') # menghapus html tag
# hapus_abusive = "|".join(map(re.escape, list(kata_abusive))) # menghapus kata abusive berdasarkan kamus abusive
tanda_baca = re.compile(r'(\W)\1+|[@#$%^&;]') # menghapus tanda baca lebih dari satu
non_latin_regex = re.compile(r'[^\x00-\x7F]+') # menghapus huruf latin yang tidak terbaca
karakter_khusus_regex = re.compile(r'[@$%^&;]') # menghabus karakter kusus
kuote_belakang = re.compile(r"\'$") # single quote di belakang
emoji_regex = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF]")