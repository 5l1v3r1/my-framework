untuk penambahan deskripsi file dan default parameter
bisa dilihat didalam file modules/form_parser.py

function wajib agar module bisa dibaca oleh interpreter:
>>> def __zvm__(url): # bisa menambahkan parameter maupun
>>>                   # logging di dalamnya
>>>     """
>>>     ini bagian untuk default parameternya
>>>     :> url: https://github.com/zevtyardt/my-framework
>>>     """
>>>     # do something <-- script yang mau dieksekusi -->
>>>

dan untuk deskripsi dari parameter dapat ditambahkan
didalam file conf.ini dengan format <param> = <deskripsi>

TODO: dapat menambahkan nama author di setiap module
      * tambahkan dibawah deskripsi module

>>> # desc: this is my module
>>> # author: zvtyrdt.id

==========================================================

untuk sementara baru ada sedikit modules, buat yang mau
berkontribusi dalam project ini bisa membaca dasarnya
terlebih dahulu. disini

https://www.petanikode.com/github-workflow/

==========================================================
