import requests
import subprocess


def run(cmd):
    completed = subprocess.run(["powershell.exe","-Command", cmd], capture_output=True)
    return completed.stdout.decode("utf-8").strip()

accessToken="Snipe IT API Key Here"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer "+accessToken,
    "content-type": "application/json"
}
urlprefix='http://snipe-it.url/api/v1'
    

def get_manufacturer(indent):
    indent=indent+1
    print(indent,'get_manufacturer')
    url = urlprefix+'/manufacturers?name='+manufacturer
    response = requests.get(url, headers=headers)
    data=response.json()
    try:
        if(data['total']!=0):
            print(indent,'get_manufacturer success')
            return data['rows'][0]['id']
    except:
        print(indent,'get_manufacturer failed')
        return -1
    print(indent,'get_manufacturer failed')
    return -1

def post_manufacturer(indent):
    indent=indent+1
    print(indent,'post_manufacturer')
    url = urlprefix+'/manufacturers'
    payload = {'name':manufacturer}
    response = requests.post(url, json=payload, headers=headers)
    data=response.json()
    if(data['status']=='success'):
        print(indent,'post_manufacturer success')
        return True
    print(indent,'post_manufacturer failed')
    return False

def get_assetnumber(indent):
    indent=indent+1
    print(indent,'get_assetnumber')
    print(indent,'get_assetnumber returning serialnumber')
    return serialnumber
    
    
def post_model(indent):
    indent=indent+1
    print(indent,'post_model')
    if (get_manufacturer(indent)==-1):
        if(not post_manufacturer(indent)):
            return False
    url=urlprefix+'/models'
    payload = {
    "name": model,
    "model_number": modelno,
    "category_id": 2,
    "manufacturer_id": get_manufacturer(indent),
    "fieldset_id": 2
    }
    response = requests.post(url, json=payload, headers=headers)
    data=response.json()
    if(data['status']=='success'):
        print(indent,'post_model success')
        return True
    print(indent,'post_model failed')
    return False

def get_model(indent):
    indent=indent+1
    print(indent,'get_model')
    url = urlprefix+'/models?limit=1&search='+model+'&sort=name'
    response = requests.get(url, headers=headers)
    data=response.json()
    try:
        if(data['total']!=0):
            print(indent,'get_model success')
            return data['rows'][0]['id']
    except:
        print(indent,'get_model failed')
        return -1
    print(indent,'get_model failed')
    return -1

#test function do not use
def get_fieldset(indent):
    indent=indent+1
    url = urlprefix+'/fieldsets'
    response = requests.get(url,headers=headers)
    data=response.json()
    print(data)


def get_hardware(indent):
    indent=indent+1
    print(indent,'get_hardware')
    url=urlprefix+'/hardware/byserial/'+serialnumber+'?deleted=false'
    response = requests.get(url, headers=headers)
    data=response.json()
    try:
        if(data['total']!=0):
            print(indent,'get_hardware success')
            return data['rows'][0]['id']
    except:
        print(indent,'get_hardware failed')
        return -1
    print(indent,'get_hardware failed')
    return -1

def post_hardware(indent):
    indent=indent+1
    if (get_model(indent)==-1):
        if(not post_model(indent)):
            print(indent,'post_hardware failed')
            return False

    url = urlprefix+'/hardware'
    payload = {'serial':serialnumber,
               'name':hostname,
               'asset_tag':get_assetnumber(indent),
               'status_id':2,
               'model_id':get_model(indent),
               'company_id':1,
               '_snipeit_mac_address_1':macaddresses,
               '_snipeit_ram_2':ramavailable,
               '_snipeit_os_3':os,
               '_snipeit_os_install_date_4':osinstalldate,
               '_snipeit_ip_address_5':ipaddress,
               '_snipeit_total_disks_size_6':disksize,
               '_snipeit_disks_info_7':diskinfo,
               '_snipeit_processor_8':processor,
               '_snipeit_bitlocker_keys_10':bitlocker}
    response = requests.post(url, json=payload, headers=headers)
    data=response.json()
    if(data['status']=='success'):
        print(indent,'post_hardware success')
        return True
    print(indent,'post_hardware failed')
    return False
    

def patch_hardware(indent):
    indent=indent+1
    print(indent,'patch_hardware')
    if (get_model(indent)==-1):
        if(not post_model(indent)):
            print(indent,'patch_hardware failed')
            return False

    url = urlprefix+'/hardware/'+str(get_hardware(indent))
    payload = {'serial':serialnumber,
               'name':hostname,
               'model_id':get_model(indent),
               'company_id':1,
               '_snipeit_mac_address_1':macaddresses,
               '_snipeit_ram_2':ramavailable,
               '_snipeit_os_3':os,
               '_snipeit_os_install_date_4':osinstalldate,
               '_snipeit_total_disks_size_6':disksize,
               '_snipeit_disks_info_7':diskinfo,
               '_snipeit_processor_8':processor,
               '_snipeit_bitlocker_keys_10':bitlocker}
    response = requests.patch(url, json=payload, headers=headers)
    data=response.json()
    if(data['status']=='success'):
        print(indent,'patch_hardware success')
        return True
    print(indent,'patch_hardware failed')
    return False


manufacturer=run("(gwmi win32_computersystem).manufacturer")
print('manufacturer ',manufacturer)

serialnumber=run("(gwmi win32_baseboard).serialnumber")
#Specific Condition for Dell
if(manufacturer=='Dell Inc.'):
    serialnumber=serialnumber.split('/')[1]
elif(manufacturer=='HP'):
    serialnumber=run('(gwmi win32_bios).serialnumber')
print('serialnumber',serialnumber)

hostname=run("(Get-WmiObject Win32_OperatingSystem).CSName")
print('hostname',hostname)

#static binding as these laptops dont have serial number written their baseboard
if(hostname=="HOSTNAME1"):
    serialnumber="SERIALNUMBER1"
if(hostname=="HOSTNAME2"):
    serialnumber="SERIALNUMBER2"


os=run("(Get-WmiObject Win32_OperatingSystem).Caption")
print('os',os)

ramavailable=run("[Math]::Round((Get-WmiObject Win32_ComputerSystem).totalphysicalmemory / 1gb,1)")
print('ramavailable',ramavailable)

osinstalldate=run("Get-CimInstance Win32_OperatingSystem | Select-Object  InstallDate | ForEach{ $_.InstallDate }")
print('osinstalldata',osinstalldate)

modelno=run("(gwmi win32_baseboard).product")
print('modelno',modelno)

model=run("(Get-WmiObject -Class:Win32_ComputerSystem).Model")
print('model',model)

if(manufacturer=='Lenovo'):
    modelno,model=model,modelno

ipaddress=run("(Test-Connection (hostname) -count 1).IPv4Address.IPAddressToString")
print('ipaddress',ipaddress)

disksize=run("""
$total=0
(Get-WmiObject -Class Win32_DiskDrive | Where-Object { $_.MediaType -eq 'Fixed hard disk media' }).Size | foreach-object { $total=$total+$_/1gb }
[Math]::Round($total, 2)
""")


print('disksize',disksize)

diskinfo=run("""
(Get-WmiObject -Class Win32_DiskDrive | Where-Object { $_.MediaType -eq 'Fixed hard disk media' }) | ForEach-Object{
    echo "$($_.MediaType) - $($_.Model) - $($_.SerialNumber) - $([Math]::Round($_.Size/1gb,2)) GB"
}
""")
print('diskinfo',diskinfo)

##diskserialnumber=run("(gwmi win32_diskdrive).serialnumber.trim()")
#macaddresses=run("(Get-WmiObject Win32_NetworkAdapterConfiguration | where {$_.ipenabled -EQ $true}).Macaddress")
macaddresses=run("""
Get-NetAdapter | ForEach-Object { $_.Name + " " + $_.MacAddress }
""")
print('macaddresses',macaddresses)

processor=run("(gwmi Win32_processor).name")
print('processor',processor)

bitlocker=run("""
Get-BitLockerVolume |
    ForEach-Object {
        $_.MountPoint + " " + $_.VolumeStatus + " " + $_.KeyProtector.RecoveryPassword + " " + $_.KeyProtector.NumericalPassword + " " + $_.KeyProtector.TPMandPIN
        }
""")
print('bitlocker',bitlocker)


if(get_hardware(1)==-1):
    print(post_hardware(1))
else :
    print(patch_hardware(1))

