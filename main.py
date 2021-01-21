#Re: librería para manejo de expresiones regulares
#Sys: Librería para manejo de sistema
import re
#import sys

#Diccionario con expresiones regulares de sentencias SQL.
#Keys -> Nombre de SQL SENTENCE
#Values -> Expresión regular de SQL SENTENCE
regex_dictionary = {
    "create database" : r"^(CREATE DATABASE|create database) ([A-Za-z][\w]*);?",
    "use" : r"^(USE|use) ([A-Za-z][\w]*);?",
    "create table" : r"^(CREATE TABLE|create table) [A-Za-z][\w]* (\([A-Za-z][\w]* (varchar\(\d+\)|int|bit)(, [A-Za-z][\w]* (varchar\(\d+\)|int|bit))*)\);?",
    "insert" : r"^(INSERT INTO|insert into) [A-Za-z][\w]* (VALUES|values) \((null|true|false|\d+|\'[ \w]+\')((,(null|true|false|\d+|\'[ \w]+\')))*\);?",
    "select" : r"^(SELECT|select) ([A-Za-z]([\w]*)(, [A-Za-z][\w]*)*|\*) (FROM|from) ([A-Za-z]([\w])*)( (where|WHERE) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\')( (AND|and) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\'))*)?;?",
    "delete" : r"^(DELETE|delete) (FROM|from) ([A-Za-z]([\w])*)( (where|WHERE) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\')( (AND|and) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\'))*)?;?",
    "update" : r"^(UPDATE|update) ([A-Za-z]([\w]*)(, [A-Za-z][\w]*)*|\*) (SET|set) ([A-Za-z]([\w])*) = (null|true|false|\d+|\'[ \w]+\')(, ?([A-Za-z]([\w])*) = (null|true|false|\d+|\'[ \w]+\'))?( (where|WHERE) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\')( (AND|and) ([A-Za-z]([\w]*)) = (null|true|false|\d+|\'[ \w]+\'))*)?;?"
}

#inyection une los argumentos enviados a través de línea de comandos
#inyection = " ".join(sys.argv[1:])
#bandera isSqlSentence que cambia en caso de que se inserte una sentencia SQL
#Se analiza el valor de cada llave del diccionario, comparándolo con el valor ingresado desde la consola. 
#Si existe un resultado, se indica el tipo de sentencia y su valor.
def test(sentence, operation):
    for key, value in regex_dictionary.items():
        result = re.search(value, sentence)
        #If operation is true, then the code evalu
        if result != None and operation is True:
            #print(f"Alert! Someone wanted to insert a SQL sentence : {key}\nThe operation was: {result.group()}, but your favorite program stopped the attack. :)")
            return key, result.group()
        if result != None and operation is False:
            #print(f"You're executing a SQL sentence : {key}\nThe operation was: {result.group()} :)")
            return key, result.group()
    return None


