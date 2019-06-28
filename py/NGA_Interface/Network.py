
import  httplib

from NGA_Utils.Xml_Import import NGA_Xml_Import

class NGA_Interface_Network:

    url = 'www.nexgenarrays.com'
    enabled = False
    
    def __init__(self):

        self.enabled = False
        try:
            conn = httplib.HTTPConnection(self.url)
            conn.request("GET", "/")
            r1 = conn.getresponse()
            print r1.status, r1.reason
            print r1.getheader('Location')
            enabled = True
            self.xml_parse()
        except:
            print "NET: Network Error"
       
    
    
    def xml_parse(self):
        xml = NGA_Xml_Import()

if __name__ == '__main__':
    net = NGA_Interface_Network()
