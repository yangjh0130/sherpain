import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, dump
import openpyxl

xmlfile_name_dir = 'C:/Users/YJH/Desktop/python/tenable/plugin_xml_to_xlsx/NetworkscanWASdisabled.1000045 (2).xml'

xl = openpyxl.Workbook()
sheet = xl.active

def xml_file():
    
    tree = ET.parse(xmlfile_name_dir)

    xml_plugin = tree.find('Policy').find('IndividualPluginSelection')

    sheet["A"+str(1)] = str("ID")
    sheet["B"+str(1)] = str("Name")
    sheet["C"+str(1)] = str("Family")
    
    for i in range(len(xml_plugin)):
        sheet["A"+str(i+2)] = xml_plugin[i][0].text
        sheet["B"+str(i+2)] = xml_plugin[i][1].text
        sheet["C"+str(i+2)] = xml_plugin[i][2].text


    xl.save('C:/Users/YJH/Desktop/python/tenable/plugin_xml_to_xlsx/plugin_xml_list.xlsx')
    xl.close()

xml_file()
