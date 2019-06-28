'''
Created on Feb 1, 2014

@author: dfreedman
'''
import xml.etree.ElementTree as et
import csv

class NGA_Xml_Import:

    xmltext1 = """
    <dicts>
        <key>1375</key>
        <dict>
            <key>Key 1</key><integer>1375</integer>
            <key>Key 2</key><string>Some String</string>
            <key>Key 3</key><string>Another string</string>
            <key>Key 4</key><string>Yet another string</string>
            <key>Key 5</key><string>Strings anyone?</string>
        </dict>
    </dicts>
    """
    
    xmltext = """
    <iris>
        <spot>
            <key>1000</key>
            <probe>13F6</probe>
            <info>
                <x-pos>1000</x-pos>
                <y-pos>1000</y-pos>
                <radius>50</radius>
            </info>
        </spot>
        <spot>
            <key>1001</key>
            <probe>8G5</probe>
            <info>
                <x-pos>1250</x-pos>
                <y-pos>1350</y-pos>
                <radius>60</radius>
            </info>
        </spot>
    </iris>
    """
    
    def __init__(self):
        self.test_xml()
        
    def test_xml(self):
        f = open('output.txt', 'w')
    
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        
        tree = et.fromstring(self.xmltext)
        
        # iterate over the dict elements
        if (tree.tag == "iris"): #sanity check
            for spot_el in tree.iterfind('spot'):
                data = []
                # get the text contents of each non-key element
                for el in spot_el:
                    if el.tag == 'key':
                        data.append(el.text)
                    # if it's an integer element convert to int so csv wont quote it
                    elif el.tag == 'probe':
                        data.append(el.text)
                for info_el in spot_el.iterfind('info'):
                    for in_el in info_el:
                        print in_el.tag + ":" + in_el.text
                writer.writerow(data)
                
        f.close()