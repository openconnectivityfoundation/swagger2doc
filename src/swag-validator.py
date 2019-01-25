#!/usr/bin/env python 
# 
# This program is free software; you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation; either version 2 of the License, or (at your 
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for 
# the full text of the license. 
#
# TODO
# 
#
# FIXES
# - 

 
import time 
import os    
import json
import random
import sys
import argparse
import traceback
from datetime import datetime
from time import gmtime, strftime
from jsonschema import validate
import jsonschema

 
if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" % (sys.version_info[0], sys.version_info[1]))

    
def find_key(rec_dict, target, depth=0):
    """
    find key "target" in recursive dict
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    #print ("find key", target);
    try:
        if isinstance(rec_dict, dict):
            for key, value in rec_dict.items():
                if key == target:
                    return rec_dict[key]
            for key, value in rec_dict.items():
                r = find_key(value, target, depth+1)
                if r is not None:
                        return r
        #else:
        #    print ("no dict:", rec_dict)
    except:
        print("xxxxx")
        traceback.print_exc()
        
def validate_with_ref(jsonfile, schema_data_reference, example_data):
    schema_data = None
    ref = None
    try:
        try:
            #print ("  validate_with_ref : full ref :", schema_data_reference)
            ref = schema_data_reference.get("$ref")
            reference = ref.replace('#/definitions/', '')
            print ("  validate_with_ref : ref :", reference)
            definitions_dict = jsonfile.get("definitions")
            #schema_data = find_key(definitions_dict, reference)
            schema_data = definitions_dict.get(reference)
            print ("  validate_with_ref : schema :", schema_data)
        except:
            print ("ERROR1: with ",schema_data_reference)
            
        try: 
            validate_data(schema_data, example_data)
            print("  validation: OK\n")
        except jsonschema.exceptions.ValidationError as ve:
            print("Record #{}: ERROR\n".format(schema_data))
            print(str(ve) + "\n")
            pass
            
    except:
        print ("ERROR: with ",schema_data_reference)
        print ("     : with ",schema_data)
        traceback.print_exc()
        
def validate_data(schema_data, example_data):
    validate(example_data, schema_data)
        
       
def validate_body(json_dict, method, method_data):
    params = method_data["parameters"]
    
    schema_file = None
    example_data = None
        
    for param in params:
        #print (param)
        if param.get("in") == "body":
            try:           
                schema_file = param.get("schema")
            except:
                pass
            try: 
                example_data = param.get("x-example", None)
            except:
                pass
            if example_data is None:
                return
            if schema_file is None:
                return
            print ("    validating body:")
            print ("      schema file: ",schema_file)
            print ("      example_data: ",example_data)
            validate_with_ref (json_dict, schema_file, example_data )
    
def printKeysOfDict(method_data, prefix ="    key :"):
    try: 
        if isinstance(method_data, dict) :
            for key, items in method_data.items():
                print (prefix, key)
    except:
        print ("printKeysOfDict : error", method_data)
            
#
#   main of script
#
print ("*****************************")
print ("*** swag-validator (v1.1) ***")
print ("*****************************")
parser = argparse.ArgumentParser()

parser.add_argument( "-ver"        , "--verbose"     , help="Execute in verbose mode", action='store_true')
parser.add_argument( "-file"       , "--file"       , default=None, help="swagger file name",  nargs='?', const="", required=False)

args = parser.parse_args()

print("file        : " + str(args.file))

try:
    schema_string = open(args.file, 'r').read()
except:
    print ("swag-validator *** ERROR : could not open:", args.v)
    
try:
    json_dict = json.loads(schema_string)
except:
    print ("swag-validator *** ERROR : error in JSON:", args.file)
    traceback.print_exc()
    try:
        print (json_dict)
    except:
        print ("error in ", args.file)
        pass
    
for pathname, path in json_dict.get("paths").items() :
    print ("path : ", pathname)
    for method, method_data  in path.items():
        print ("  method :", method)
        
        if method in [ "put", "post", "patch"]:
            validate_body(json_dict, method, method_data)
        
        # loop over all responses
        for response_name, responses in method_data["responses"].items():
            try:
                schema_file = None
                example_data = None
                
                schema_file = responses.get("schema",None)
                example_data = responses.get("x-example",None)
                print ("  response : ", response_name)
                print ("    schema file: ",schema_file)
                print ("    example_data: ",example_data)
                if schema_file is not None:
                  if example_data is not None:
                    validate_with_ref(json_dict, schema_file, example_data )
            except:
                pass
print("done!")


