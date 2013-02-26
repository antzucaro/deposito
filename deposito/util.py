import hashlib

def md5sum(filename):
    try:
        infile = open(filename, "rb")
        md5 = hashlib.md5()
        buffer = infile.read(2 ** 20)
        while buffer:
            md5.update(buffer)
            buffer = infile.read(2 ** 20)
        #infile.close()
        return md5.hexdigest()
    except Exception as e:
        print e
        return None
