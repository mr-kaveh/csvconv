# csvconv
CSV Converter 

In order to execute the code, make sure that python3 is installed with the following commands: 

## `$ sudo apt update && sudo apt upgrade $ sudo apt install python3`

Then install python3-pip and ruamel.yaml library with the following commands: 

## `$ sudo apt install python3-pip $ sudo pip3 install ruamel.yaml`

After that in the directory which contains the code issue the following command:

## `$ python3 converter.py –h`

Examples of execution: 

## `$python3 converter.py hotels.csv hotels_db.db sql -v`
## `$python3 converter.py hotels.csv hotels_yaml.yml yml -v`
## `$python3 converter.py hotels.csv hotels_html.html html -v`
## `$ python3 converter.py hotels.csv hotels_xml.xml xml -v`
## `$ python3 converter.py hotels.csv hotel_json.json json -v`

As you can see all the required formats are supported by the code, I have created 2 custom classes one for custom log handling which creates a log file in the present working directory as the code and handles DEBUG, ERROR and CRITICAL logs. The other class parses the positional and optional arguments.

The converter.py has 11 defined functions which are executed in 2 phases which are started with the execution of main() method . in main(), the method get_input_files(args.input) is executed which reads the input file hotels.csv and starts validation of hotel names, stars and urls and writes the validated and other fields of hotels.csv file to hotels.csv.tmp file. This way the original data will be intact and the temporary file is used in conversion process. more detailed information about parameters and validation process is available in the code.

Second phase is the conversion, which starts by passing the format argument to convert_manager(args.format) method and depending on the required format , the appropriate method will be called.

