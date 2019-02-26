# ini untuk deskripsi modulenya
# desc: this is hmmmmmmm

def run(string, logging):
    logging.info(string)

# ini wajib
# fungsi __init__ buat awalan nya, wajib diisi satu parameter atau lebih
def __init__(string, logging): # bisa menambahkan parameter logging kalau mau ganti print jadi logging
    """
    Ini untuk default value nya , format samain kek dibawah
    Semua parameter wajib diisi selain logging, None untuk value kosong
    
    :> string: default value
    """
    run(string, logging)
