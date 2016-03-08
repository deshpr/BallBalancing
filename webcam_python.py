
import cv2
import urllib2
import numpy as np
import sys


hoststr = "192.168.1.6:1069"

hoststr = "http://" + hoststr + '/video'

print "Streaming " + hoststr

stream = urllib2.urlopen(hoststr)

bytes_data = ''
while True:
    bytes_data += stream.read(1024)
    a = bytes_data.find('\xff\xd8')
    b = bytes_data.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes_data[a:b + 2]
        bytes_data = bytes_data[b+2:]
        print('remaining byts data = {0}'.format(bytes_data))
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow(hoststr, i)
        if cv2.waitKey(1) == 27:
            exit(0)