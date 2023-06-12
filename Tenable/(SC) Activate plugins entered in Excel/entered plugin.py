import pandas as pd
import os
from tenable.sc import TenableSC
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, dump

scriptfile_dir = 'C:/Users/YJH/Desktop/python/new'
plugin_file_name = 'plugin-list.xlsx'
SC_ip = '192.168.1.232'
SC_port = 443
SC_id = 'admin'
SC_pw = 'sh#Rpa1n'
xmlfile_name_dir = 'c:/Users/YJH/Desktop/python/new/test1.xml'

def plugin_list():

    os.chdir(scriptfile_dir)
    enable_plugin_file = pd.read_excel(plugin_file_name)

    df = pd.DataFrame(enable_plugin_file)

    plugin_list = df.values.tolist()

    return(plugin_list)


def plugin_info():

    sc = TenableSC(SC_ip, port=SC_port)
    sc.login(SC_id, SC_pw)

    p_name = []
    p_family = []
    p_id = []

    for i in plugin_list():
        plugin = sc.plugins.details(i[0])

        p_name.append(plugin['name'])
        p_family.append(plugin['family']['name'])
        p_id.append(plugin['id'])

    return(p_name, p_family, p_id)

def xml_file():
    
    tree = ET.parse(xmlfile_name_dir)

    xml_family = tree.find('Policy').find('FamilySelection').findall('FamilyItem')
    
    plugin_info1 = plugin_info()

    for i in plugin_info1[1]:
        for k in xml_family:
            if k[0].text == i:
                k[1].text = 'mixed'
    
    xml_plugin = tree.find('Policy').find('IndividualPluginSelection')

    for j in range(len(plugin_info1[0])):
        node1 = Element("PluginItem")

        node2 = Element("PluginId")
        node2.text = str(plugin_info1[2][j])

        node3 = Element("PluginName")
        node3.text = str(plugin_info1[0][j])

        node4 = Element("Family")
        node4.text = str(plugin_info1[1][j])

        node5 = Element("Status")
        node5.text = "enabled"

        xml_plugin.append(node1)
        node1.append(node2)
        node1.append(node3)
        node1.append(node4)
        node1.append(node5)

        tree.write(xmlfile_name_dir)

    print("Done")

xml_file()
