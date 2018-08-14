# swagger2doc

swagger2doc tool

This tool creates the documentation for an OCF derived model resource in a supplied word document.
The tools needs to be called for each derived model that needs to be added to the word document.

The calling order is specific for each document.

# Derived Model input parameters

Typical input:
```
python3 -docx <word file> --derived <derived eco system name> -swagger <json schema of the derived model> -word_out <word output file>
```

- -docx  <>

    input word file: start of the word file
- -derived <>

    name of the derived eco system: for example: Alljoyn
- -swagger <>

    name of the json derived model name, this is ONLY the json definition
- -word_out <>

    word file with the appended data
    
# folder processing

In the folder test there is a script that can process multiple files in a folder.
The script is called ```derive_folder.sh```

typical usage:
```
 sh derive_folder.sh <input folder> <output folder> <eco system> <input word file>
```

- input folder

    folder where the json files recides.
    
- output folder

    folder to be used to generate the output tool
    
- eco system name   

    name to be used in the tables
    
- input word file

    optional, word file that is used to append the sections too. input file is NOT changed.

    
# example of derived model in json schema format

<-- annotation of what is needed/interpreted by the tooling.

```
{
  "id": "http://openinterconnect.org/asamapping/schemas/asa.environment.currentairquality.json#",
  "$schema": "http://json-schema.org/draft-04/schema#",
  "description" : "Copyright (c) 2018 Open Connectivity Foundation, Inc. All rights reserved.",
  "title": "my derived model name",                                                        <-- name of the section
  "definitions": {
    "my_derived_model_1": {                                                                <-- name of the derived type
      "description" : "the my_derived_model_1 description (single line)",
      "properties": {
        "prop1": {                                                                         <-- property name of the derived eco system
          "type": "integer",                                                               <-- type of the property 
          "description": "prop1 description",                                              <-- description of the property
          "x-ocf-conversion": {
            "x-ocf-alias": "oic.r.airquality",                                             <-- ocf resource type mapping
            "x-to-ocf": [                                                                  <-- rule to ocf (string array)
              "valuetype = Measured",
              "contaminanttypearray = [CH2O,CO2,CO,PM2_5,PM10,VOC]",
              "ocf.contaminanttype = contaminanttypearray[contaminanttype]"
            ],
            "x-from-ocf": [                                                                <-- rule from ocf (string array)
              "valuetype = Measured",
              "contaminanttype = indexof contaminanttypearray[ocf.contaminanttype]"
            ]
          }
        },
        "prop2": {
          "type": "number",
          "description": "prop2 description",
          "x-ocf-conversion": {
            "x-ocf-alias": "oic.r.airquality",
            "x-to-ocf": [
              "contaminantvalue = currentvalue"
            ],
            "x-from-ocf": [
              "currentvalue = contaminantvalue"
            ]
          }
        }
      }
    },
    
    "my_derived_model_2": {                                                                <-- name of the 2nd derived type
      "description" : "the my_derived_model2 description\n line2",
      "type": "object",
      "properties": {
        "xxxx": {
          "type": "integer",
          "description": "The contaminant type",
          "x-ocf-conversion": {
            "x-ocf-alias": "oic.r.airquality",
            "x-to-ocf": [
              "valuetype = Measured",
              "contaminanttypearray = [CH2O,CO2,CO,PM2_5,PM10,VOC]",
              "ocf.contaminanttype = contaminanttypearray[contaminanttype]"
            ],
            "x-from-ocf": [
              "contaminanttype = indexof contaminanttypearray[ocf.contaminanttype]"
            ]
          }
        },
        "yyy": {
          "type": "number",
          "x-ocf-conversion": {
            "x-ocf-alias": "oic.r.airquality",
            "x-to-ocf": [
              "contaminantvalue = currentvalue"
            ],
            "x-from-ocf": [
              "currentvalue = contaminantvalue"
            ]
          }
        }
      }
    }
    
    
    
  },
  "type": "object",
  "allOf": [
    {"$ref": "#/definitions/my_derived_model_1"},
    {"$ref": "#/definitions/my_derived_model_2"}
  ],
  "required": ["prop1", "yyy"]                                                             <-- required properties 
}
```