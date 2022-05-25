from django.contrib import messages

def has_minimal_length(field,minLength):
    return len(field) >= minLength

def has_some_string_char(field,string):
    for char in field:
        if char in string:
            return True
    return False

def empty_field(field):
    """Return true if field has only spaces or it is empty"""
    return not field.strip()

def validated_fields(fields,request):
    validated = True
    strings = [
        {'string':'abcdefghijklmnopqrstuvxzwç','type':'caractere minúsculo'},
        {'string':'ABCDEFGHIJKLMNOPQRSTUVXZWÇ','type':'caractere maiúsculo'},
        {'string':'1234567890','type':'número'},
        {'string':'!@#$%¨&*()_+-{}[]:;.>,<\\|/?\"\'¹²³£¢¬§ªº','type':'caractere especial'}
    ]

    if empty_field(fields['username']) or empty_field(fields['limit_visits']) or empty_field(fields['limit_datetime']):
        messages.error(request,"Nenhum campo pode estar em branco.")
        validated = False
    if not has_minimal_length(fields['password'],8):
        messages.error(request,"A senha deve ter pelo menos 8 caracteres.")
        validated = False
    for type_string in strings:
        if not has_some_string_char(fields['password'],type_string['string']):
            messages.error(request,f"A senha deve conter pelo menos um {type_string.type}.")
            validated = False

    return validated

