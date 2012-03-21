#!/usr/bin/env python
# -*- coding:utf-8 -*-

import struct, os


def get_file_hash(name):
    try:
        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(name, "rb")

        filesize = os.path.getsize(name)
        hash_value = filesize

        if filesize < 65536 * 2:
           return "SizeError"

        for x in range(65536/bytesize):
            content_buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, content_buffer)
            hash_value += l_value
            hash_value = hash_value & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number


        f.seek(max(0,filesize-65536),0)
        for x in range(65536/bytesize):
            content_buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, content_buffer)
            hash_value += l_value
            hash_value = hash_value & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash =  "%016x" % hash_value
        return returnedhash
    except IOError:
        return "IOError"
