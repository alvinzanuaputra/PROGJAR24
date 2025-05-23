import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
    
    def upload(self, params=[]):
        try:
            filename, filecontent = params[0], params[1]
            if os.path.exists(filename):
                return dict(status='ERROR', data=f'File "{filename}" sudah tersedia dalam direktori')
            with open(filename, 'wb') as fp:
                fp.write(base64.b64decode(filecontent.encode()))
            return dict(status='OK', data=f'{filename} berhasil diupload ke server')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def hapus(self, params=[]):
        try:
            filename = params[0]
            if not os.path.exists(filename):
                return dict(status='ERROR', data=f'File "{filename}" tidak ditemukan dalam direktori')
            os.remove(filename)
            return dict(status='OK', data=f'{filename} berhasil dihapus dari server')
        except Exception as e:
            return dict(status='ERROR', data=str(e))



if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
