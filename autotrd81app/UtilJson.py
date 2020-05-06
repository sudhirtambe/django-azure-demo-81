#This module does all json related operations

import json

#Pass hierarchical key values to retrive nested value
def getNestedConfigItem(dictData, *args):
    if args and dictData:
        element  = args[0]
        if element:
            value = dictData.get(element)
            return value if len(args) == 1 else getNestedConfigItem(value, *args[1:])
