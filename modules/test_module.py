# ini untuk deskripsi modulenya
# desc: this is hmmmmmmm

def run(string, logging):
    logging.info(string)

# fungsi ini buat base nya, wajib diisi satu parameter atau lebih
def __init__(string, logging): # bisa menambahkan parameter logging kalau mau ganti print jadi logging
    """
    Ini untuk default value nya , format samain kek dibawah
    :> string: default value
    """
    run(string, logging)
