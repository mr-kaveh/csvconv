#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import csv
import logging
import custom_log
import arg_parser
import os
import codecs
import re
import json
import sys
import sqlite3
from ruamel.yaml import YAML

# Instantiating custom_log and arg_parser class
log = custom_log.clog().propagate_logger()
args = arg_parser.parser().propagate_args()


def get_input_file(file_name: str) -> None:
    """
    reads and validates the input file, it also creates
    a copy of input file in which all the data is validated
    a ready to convert
    :param file_name: input file name
    :return: none
    """
    log.info("Starts Reading The Input file")
    try:
        with open(file_name, "r") as csv_file, \
                open(file_name + ".tmp", "w") as tmp_file:
            csv_writer = csv.writer(tmp_file, delimiter=',', escapechar=' ')
            csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
            log.info("Starts Reading the contents of the csv")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    csv_writer.writerow(row)
                    line_count = line_count + 1
                hotel_name = validate_hotel_names(row["name"])
                address = row["address"]
                stars = validate_hotel_stars(int(row["stars"]))
                contact = row["contact"]
                phone = row["phone"]
                url = validate_hotel_urls(row["uri"])
                csv_writer.writerow([hotel_name, address, stars, contact, phone, url])
    except EnvironmentError:
        log.critical("IO Error: Reading Input CSV File / Writing Output CSV Temp File")


def validate_hotel_names(hotel_name: str) -> str:
    """
    validates if the hotel name encoding is utf-8,
    and in case it is not, it encodes it to utf-8
    :param hotel_name: hotel_name from input file
    :return hotel_name: utf-8 encoded hotel_name
    """
    log.info("Starts Validating hotel_name for hotel " + hotel_name)
    if all(ord(char) < 128 for char in hotel_name):
        log.info("hotel_name coding is utf-8 for hotel " + hotel_name)
        return hotel_name
    log.info("hotel_name coding is not utf-8 for hotel " + hotel_name)
    log.info("Encoding " + hotel_name + " to utf-8")
    return hotel_name.encode('utf-8')


def validate_hotel_urls(url: str) -> str:
    """
    checks if the hotel url is valid by using
    regular expression,another way of validating
    urls is to use urllib.urlopen(urllib2.request("http://hotel.com"))
    and check if there is any urllib2.HTTPError
    Exception occurs.
    :param url: url of the hotel website
    :return: Either the url in case it is valid or
    an appropriate message in case of invalidity
    """
    log.info("Starts Validating the url for " + url)
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'  # domain...
        r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, url) is not None:
        return url
    else:
        log.info("uri " + url + " is not valid")
        return url + " is not a valid url"


def validate_hotel_stars(stars: int) -> int:
    """
    Checks if the range of hotel rate(stars)
    is between 0 and 5(5 is considered valid)
    No negative number is allowed
    :param stars: Hotel Rate
    :return stars: Valid non negative value
    for hotel rate
    """
    log.info("Starts Validating the hotel rate for the value " + str(stars))
    if stars < 0:
        stars = 0
    elif stars > 5:
        stars = 5
    else:
        return stars
    return stars


def convert_to_xml(csv_file: str, xml_file: str) -> None:
    """
    Converts the csv formatted input file to xml format
    :param csv_file: The name of Validated csv file which
    resides in the present working directory
    :param xml_file: The name of xml formatted output which
    will be saved in the present working directory
    :return: Nothing
    """
    try:
        with open(csv_file, "r"), \
             open(xml_file, "w") as xml_data:
            csv_data = csv.reader(open(csv_file))
            xml_data.write('<?xml version="1.0"?>' + "\n")
            xml_data.write('<csv_data>' + "\n")
            row_num = 0
            log.info("starts converting to XML Format")
            for row in csv_data:
                if row_num == 0:
                    tags = row
                    for i in range(len(tags)):
                        tags[i] = tags[i].replace(' ', '_')
                else:
                    xml_data.write('<row>' + "\n")
                    for i in range(len(tags)):
                        xml_data.write('    ' + '<' + tags[i] + '>' \
                                       + row[i] + '</' + tags[i] + '>' + "\n")
                    xml_data.write('</row>' + "\n")
                row_num += 1
            xml_data.write('</csv_data>' + "\n")
            log.info("Finished Converting to XML Format")
            xml_data.close()
    except EnvironmentError:
        log.critical("IO Error: Reading Input CSV File / Writing Output XML File")


def convert_to_json(csv_file: str, json_file: str) -> None:
    """
    Converts the csv formatted input file to json format
    :param csv_file: The name of Validated csv file which
    resides in the present working directory
    :param json_file: The name of json formatted output which
    will be saved in the present working directory
    :return: Nothing
    """
    log.info("starts converting to JSON Format")
    try:
        with open(csv_file) as csv_data, \
                open(json_file, "w") as json_data:
            reader = csv.DictReader(csv_data)
            rows = list(reader)
            json.dump(rows, json_data)
        log.info("Finished converting to JSON Format")
    except EnvironmentError:
        log.critical("IO Error: Reading Input CSV File / Writing Output JSON File")


def convert_to_yaml(csv_file: str, yaml_file: str) -> None:
    """
    Converts the csv formatted input file to yaml format
    :param csv_file: The name of Validated csv file which
    resides in the present working directory
    :param yaml_file: The name of yaml formatted output which
    will be saved in the present working directory
    :return: Nothing
    """
    log.info("starts converting to YAML Format")
    try:
        with open(csv_file, "r"), \
             open(yaml_file, "w") as yaml_data:
            csv_reader = csv.reader(open(csv_file))
            keys = next(csv_reader)
            yaml = YAML()
            yaml.indent(sequence=4, offset=2)
            for row in csv_reader:
                yaml.dump([dict(zip(keys, row))], yaml_data)
            log.info("Finished converting to YAML Format")
    except EnvironmentError:
        log.critical("IO Error: Reading Input CSV File / Writing YAML File")


def convert_to_html(csv_file: str, html_file: str) -> None:
    """
    Converts the csv formatted input file to html format
    :param csv_file: The name of Validated csv file which
    resides in the present working directory
    :param html_file: The name of html formatted output which
    will be saved in the present working directory
    :return: Nothing
    """
    log.info("starts converting to HTML Format")
    try:
        with open(csv_file, "r"), \
             open(html_file, "w") as html_data:
            csv_reader = csv.reader(open(csv_file))
            html_data.write('<title>Hotels List</title>')
            html_data.write('<table>')
            for row in csv_reader:  # Read a single row from the CSV file
                html_data.write('<tr>');  # Create a new row in the table
                for column in row:  # For each column..
                    html_data.write('<td>' + column + '</td>');
                html_data.write('</tr>')
            html_data.write('</table>')
            log.info("Finished converting to HTML Format")
    except EnvironmentError:
        log.critical("IO Error: Reading Input CSV File / Writing HTML File")


def convert_to_sqlite(csv_file: str, db_name: str) -> None:
    """
    Converts the csv formatted input file to sqllite database
    :param csv_file: The name of Validated csv file which
    resides in the present working directory
    :param db_name: The name of sqllite database file which
    will be saved in the present working directory
    :return: Nothing
    """
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS hotels(name varchar,address varchar
            ,stars int,contact varchar,phone varchar, uri varchar)""")

        with open(csv_file) as file:
            reader = csv.reader(file)
            for row in reader:
                cursor.execute("INSERT INTO hotels VALUES (?,?,?,?,?,?);", row)
        connection.commit()
    except sqlite3.Error as sqlite3_error:
        log.critical(str(sqlite3_error))
        connection.rollback()
    except Exception as exception:
        log.critical(str(exception))
    finally:
        connection.close()


def convert_manager(file_type: str) -> None:
    """
    Interfaces the Convert process based on input
    :param file_type: String input to signify for
    the script to which format should it do the conversion
    :return: Nothing
    """
    if file_type in ("xml", "XML", "Xml"):
        convert_to_xml("hotels.csv.tmp", args.output)
        if args.verbose:
            print("Conversion of %s to %s finished successfuly"
                  % ("hotels.csv.tmp", args.output))
    elif file_type in ("JSON", "json", "Json"):
        convert_to_json("hotels.csv.tmp", args.output)
        if args.verbose:
            print("Conversion of %s to %s finished successfuly"
                  % ("hotels.csv.tmp", args.output))
    elif file_type in ("YAML", "yaml", "YML", "yml"):
        convert_to_yaml("hotels.csv.tmp", args.output)
        if args.verbose:
            print("Conversion of %s to %s finished successfuly"
                  % ("hotels.csv.tmp", args.output))
    elif file_type in ("html", "HTML", "htm", "HTM"):
        convert_to_html("hotels.csv.tmp", args.output)
        if args.verbose:
            print("Conversion of %s to %s finished successfuly"
                  % ("hotels.csv.tmp", args.output))
    elif file_type in ("sql", "SQL", "sqlite"):
        convert_to_sqlite("hotels.csv.tmp", args.output)
        if args.verbose:
            print("Conversion of %s to %s finished successfuly"
                  % ("hotels.csv.tmp", args.output))


def main():
    """
    Function calls come right here,baby :)
    Firstly, get_input_file reads the hotels.csv
    and, creates a temp file called named hotels.csv.tmp
    which contains the validated csv data. validation of
    hotel names, stars and uri comes right here. in other words,
    3 functions; validate_hotel_names, validate_hotel_urls,
    validate_hotel_stars are executed through get_input_files.
    Secondly, convert_manager calls the methods to convert to all
    of the required format.
    :return: Nothing
    """
    # Input from the terminal
    # Example: python3 converter.py hotels.csv hotels.xml xml
    get_input_file(args.input)
    convert_manager(args.format)


if __name__ == "__main__":
    main()
