import re
import sys

#Dictionary with the regular expresions of SQL Sentences
regexDictionary = {
    "create database" : r"^(CREATE DATABASE|create database) ([A-Za-z][\w]*);?",
    "use" : r"^(USE|use) ([A-Za-z][\w]*);?",
    "create table" : r"^(CREATE TABLE|create table) [A-Za-z][\w]*(\([A-Za-z][\w]* (varchar\(\d+\)|int|bit)(,[A-Za-z][\w]* (varchar\(\d+\)|int|bit))*)\);?",
    "insert" : r"^(INSERT INTO|insert into) [A-Za-z][\w]* (VALUES|values) \((null|true|false|\d+|\'[ \w]+\')((,(null|true|false|\d+|\'[ \w]+\')))*\);?",
    "select" : r"^(SELECT|select) ([A-Za-z]([\w])*|\*) (FROM|from) ([A-Za-z]([\w])*)( (where|WHERE) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\')( (AND|and) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\'))*)?;?",
    "delete" : r"^(DELETE|delete) (FROM|from) ([A-Za-z]([\w])*)( (where|WHERE) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\')( (AND|and) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\'))*)?;?",
    "update" : r"fds"
}

inyection = " ".join(sys.argv[1:])

for keys, values in regexDictionary.items():
    result = re.search(values, inyection)
    if result != None:
        isSqlSentence = True
        print(f"Alert! Someone wanted to insert a SQL sentence : {keys}\nThe operation was: {result.group()}, but your favorite program stopped the attack. :)")




