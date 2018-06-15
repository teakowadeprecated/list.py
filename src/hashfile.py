import base64
import hashlib


def SHA1(fineName, block_size=64 * 1024):
    with open(fineName, 'rb') as f:
        sha1 = hashlib.sha1()
        while True:
            data = f.read(block_size)
            if not data:
                break
            sha1.update(data)
        retsha1 = base64.b64encode(sha1.digest())
        return retsha1
