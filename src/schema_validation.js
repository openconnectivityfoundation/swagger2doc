#! /usr/bin/env node

'use strict';

var commander = require('commander');
var pkg = require('./package.json');
var fs = require('fs-extra');
var Ajv = require('ajv');
//var S = require('string');
    
var ajv = Ajv(),
    validateSchema = true;
    
// Parse command line options and arguments
commander
    .version(pkg.version)
    //.usage('[options]')
    .option('-i, --input <file>', 'swagger input file (required)');

commander.on('--help', () => {
    console.log('  Validation Examples:');
    console.log('');
    console.log('    $ swagger_validation -i api.swaggger.json');
    console.log('');
});


commander.parse(process.argv);

console.log("input:            ", commander.input)

var body_methods = ["post", "put", "patch"];

function arrayContains(needle, arrhaystack)
{
    return (arrhaystack.indexOf(needle) > -1);
}

//../test/in/test_swagger_1/test_swagger_1.swagger.json
var swagger_file = fs.readFileSync(commander.input, 'utf-8');
//var swagger_file = fs.readFileSync("../test/in/test_swagger_error_1/test_swagger_1.swagger.json", 'utf-8');
//var swagger_file = fs.readFileSync("../test/in/test_swagger_1/test_swagger_1.swagger.json", 'utf-8');
//console.log (swagger_file);

var jsonContent = JSON.parse(swagger_file);

for (var path in jsonContent['paths']) {
    var path_item = jsonContent['paths'][path]
    console.log (path );
    // console.log (path_item );
    for (var method in path_item) {
        console.log ("  ",method);
        var method_data = path_item[method]
        
        if ( arrayContains(method, body_methods) == true) {
            //console.log ("     body");
            try {
                var params = method_data["parameters"]
                for ( var param in params) {
                   //console.log ("     param:", param);
                   var param_data = params[param]
                   //console.log ("     param_data:", param_data);
                   if (param_data["in"] == "body") {
                        console.log ("     body :");
                        try {
                            var example_data = param_data["x-example"]
                            var schema_ref = param_data["schema"]["$ref"];
                            var schema_id = schema_ref.replace("#/definitions/","");
                            console.log ("      schema_id :",schema_id);
                            console.log ("      example   : ",example_data);
                            var schema_data = jsonContent["definitions"][schema_id]
                            //console.log ("      schema   : ",schema_data);
                            
                            let validate = ajv.compile(schema_data);
                            let valid = validate(example_data);

                            if (!valid) {
                                console.log('JSON not matching with Schema');
                                console.log(validate.errors);
                                console.log (" ")
                                console.log ("      schema   : ",schema_data);
                            }
                            else {
                                console.log('VALID');
                            }
                        }
                         catch (err) {
                             console.log ("     body: schema or example not found");
                         }
                   }
                }
            }
            catch (err) {}
        
        }
        
        // all the responses
        for (var result_code in method_data["responses"]) {
            console.log ("    ",result_code);
            var result_data = method_data["responses"][result_code];
            var example_data = result_data["x-example"];
            var schema_ref = result_data["schema"]["$ref"];
            var schema_id = schema_ref.replace("#/definitions/","");
            console.log ("      schema_id :",schema_id);
            console.log ("      example   : ",example_data);
            var schema_data = jsonContent["definitions"][schema_id]
            //console.log ("      schema   : ",schema_data);
            
            let validate = ajv.compile(schema_data);
            let valid = validate(example_data);

            if (!valid) {
                console.log('JSON not matching with Schema');
                console.log(validate.errors);
                console.log (" ")
                console.log ("      schema   : ",schema_data);
            }
            else {
                console.log('VALID');
            }
        }
    }
}