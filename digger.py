
import _winreg


def enum_all_subkey() :
    root_key=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,'')
    key_index=0
    return_key_list=[]

    try :
        while True :
            key_name=_winreg.EnumKey(root_key,key_index)
            key_index+=1
            
            return_key_list.append(key_name)
    except :
        pass

    return return_key_list
    
def is_pseudo_protocal_key(input_key_name) :
    key=None
    
    try :
        key=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,input_key_name)
    except :  #  Cannot Open This Key ..
        return False
        
    key_index=0
    value_index=0
    exist_value=False
    exist_key=False
    
    try :
        while True :
            value_name,value_value,value_type=_winreg.EnumValue(key,value_index)
            value_index+=1
            
            if 'URL Protocol'==value_name :
                exist_value=True
    except :
        pass
    
    try :
        while True :
            key_name=_winreg.EnumKey(key,key_index)
            key_index+=1
            
            if 'shell'==key_name :
                try :
                    pseudo_protocal_command=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,input_key_name+'\\shell\\open\\command')
                    exist_key=True
                except :
                    pass
    except :
        pass
    
    if exist_value and exist_key :
        return True
    
    return False
    
def get_pseudo_protocal_shell(key_name) :
    pseudo_protocal_command_key=_winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,key_name+'\\shell\\open\\command')
    
    try :
        value_name,value_value,value_type=_winreg.EnumValue(pseudo_protocal_command_key,0)
            
        return value_value
    except :
        return '<except>'
    
if __name__=='__main__' :
    for subkey_index in enum_all_subkey() :
        if is_pseudo_protocal_key(subkey_index) :
            print subkey_index
            print '  Path:',get_pseudo_protocal_shell(subkey_index)
    
'''
# Test Case ..

print is_pseudo_protocal_key('asd')
print is_pseudo_protocal_key('tdsp')
print is_pseudo_protocal_key('telnet')
print is_pseudo_protocal_key('Tencent')
'''
