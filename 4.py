import urllib2
import sys

def strxor(a, b):
    if len(a) > len(b):
        return "".join([chr(ord(x)^ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x)^ord(y)) for (x, y) in zip(a, b[:len(a)])])

TARGET = 'http://crypto-class.appspot.com/po?er='

#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
            print 'Success!!!'
            print q

        except urllib2.HTTPError, e:
            # print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

if __name__ == "__main__":
    ct = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"

    c = [];
    c.append(ct[:16])
    c.append(ct[16:32])
    c.append(ct[32:48])
    c.append(ct[48:64])

    for i in range(0, 4):
        c[i] = c[i].dncode("hex")

    m = ["", "", ""]
    po = PaddingOracle()

    for i in range(0, 3):
        for j in range(1, 17):  # padding 0xj
            for g in range(0, 256):
                que = strxor(c[i],
                    strxor(chr(0)*(16-j)+chr(g)+m[i], chr(0)*(16-j)+chr(j)*j))
                que = que + c[i+1];
                que = que.encode("hex")
                # print que
                if(po.query(que)):
                    m[i] = chr(g)+m[i]
                    print m[i]
                    break

    print
    print
            
    for i in range(0, 3):
        print m[i]
    
