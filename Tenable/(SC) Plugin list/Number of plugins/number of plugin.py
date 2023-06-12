from tenable.sc import TenableSC
import openpyxl

sc = TenableSC('192.168.1.114', port=8443)
sc.login('admin', 'sh#Rpa1n')


xl = openpyxl.Workbook()
sheet = xl.active
i = 1
for fam in sc.plugins.family_list():

    plugins = sc.plugins.family_plugins(fam['id'])
    li = list(plugins)
    
    if li != []:
        print(str(fam['name']))
        plugins = sc.plugins.family_plugins(fam['id'])

        for plugin in plugins:
            sheet["A"+str(i+1)] = str(plugin['id'])
            sheet["B"+str(i+1)] = str(plugin['name'])
            desc = str(plugin['description']).replace("-","'-")
            desc = desc.replace("=","'=")
            sheet["C"+str(i+1)] = desc
            i+=1
        
    else: continue

xl.save('test_num.xlsx')
xl.close()

