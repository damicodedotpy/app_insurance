# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
def checker(value):
    if type(value) == list:
        return "lista"
    elif type(value) == dict:
        return "diccionario"
    elif type(value) == str:
        return "string"
    else:
        return "Tipo de dato desconocido"