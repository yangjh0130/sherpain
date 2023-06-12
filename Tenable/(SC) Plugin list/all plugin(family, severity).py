from tenable.sc import TenableSC
import openpyxl

sc = TenableSC('192.168.1.232', port=443)
sc.login('admin', 'sh#Rpa1n')

xl = openpyxl.Workbook()

for fam in sc.plugins.family_list():

    plugins = sc.plugins.family_plugins(fam['id'])
    li = list(plugins)
    
    if li != []:
        print(str(fam['name']))
        plugins = sc.plugins.family_plugins(fam['id'])
        sheet_name = (str(fam['name']))

        a = sheet_name.replace(":", "-")
        b = a.replace("/", "-")

        sheet = xl.create_sheet(b)
        
        sheet["A"+str(1)] = str("ID")
        sheet["B"+str(1)] = str("Name")
        sheet["C"+str(1)] = str("Severity")
        sheet["D"+str(1)] = str("Description")

        i = 1

        for plugin in plugins:
            riskFactor = sc.plugins.details(str(plugin['id']), fields={'riskFactor'})
               
            sheet["A"+str(i+1)] = str(plugin['id'])
            sheet["B"+str(i+1)] = str(plugin['name'])
            sheet["C"+str(i+1)] = str(riskFactor['riskFactor'])
            desc = str(plugin['description']).replace("-","'-")
            desc = desc.replace("=","'=")
            sheet["D"+str(i+1)] = desc
            i+=1
        
    else: continue

xl.save('test_severity.xlsx')
xl.close()

