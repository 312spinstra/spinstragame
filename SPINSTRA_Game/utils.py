import pygame
import json
import csv
import datetime
import random
import math
from datetime import timezone
from constants import *

#------------------------------#
# Function that reads a JSON file into a dictionary
def loadJSONFile(filepath):
    with open(filepath) as json_file:
            return json.loads(json_file.read())
#------------------------------#

#------------------------------#
# Function that reads a CSV file into an array of arrays of dictionaries
def loadCSVFile(filepath):
    rows = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
        csvfile.close()
    return rows


def loadCSVFilequestions(filepath):
    rows = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            rows.append(row)
        csvfile.close()
    return rows
#------------------------------#

#------------------------------#
# Function that writes a CSV with the provided row data
def writeCSVFile(filepath, fields, rows):
    with open(filepath, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        csvfile.close()
#------------------------------#

#------------------------------#
# Function that determines the question type based on the information provided
def determineQuestionType(questionInfo):
    questionInfo["type"] = "regular"

    # Determine the question type based on whether or not the "IncorrectAnswerX" fields have been filled out
    if (questionInfo["Incorrect1"] != '' or questionInfo["Incorrect2"] != '' or questionInfo["Incorrect3"] != ''):
            questionInfo["type"] = "multiple-choice"
            questionInfo["incorrectAnswers"] = []

            if (questionInfo["Incorrect1"] != None):
                questionInfo["incorrectAnswers"].append(questionInfo["Incorrect1"])
            if (questionInfo["Incorrect2"] != None):
                questionInfo["incorrectAnswers"].append(questionInfo["Incorrect2"])
            if (questionInfo["Incorrect3"] != None):
                questionInfo["incorrectAnswers"].append(questionInfo["Incorrect3"])

    return questionInfo
#------------------------------#

#------------------------------#
# Function that checks whether or not an answer to a question is correct    
def checkAnswer(userAnswer, questionInfo):
    if questionInfo["type"] == "regular" or questionInfo["type"] == "multiple-choice":
        if questionInfo["Answer"].lower() != userAnswer.strip().lower():
            return False
    return True
#------------------------------#

#------------------------------#
# Function that gets UTC time in seconds
def getUTCTime():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc) 
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp
#------------------------------#

#------------------------------#
# Function that encodes a number into base 36
def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        raise TypeError('number must be an integer')
 
    base36 = ''
    sign = ''
 
    if number < 0:
        sign = '-'
        number = -number
 
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
 
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
 
    return sign + base36
#------------------------------#

#------------------------------#
# Function that splits text into lines of a specified container width to make it easy to render
def prepareTextForRendering(text, fontSize, containerWidth):
    font = pygame.font.Font(GAME_FONT_PATH, fontSize)

    textToTest = text
    textWidth, _ = font.size(textToTest)

    while (textWidth >= containerWidth):
        textToTest = textToTest[:-1]
        textWidth, _ = font.size(textToTest)
    
    maxCharactersPerLine = len(textToTest)
    originalText = text

    result = [ text[i:i+maxCharactersPerLine] for i in range(0, len(originalText), maxCharactersPerLine) ]
    return result
#------------------------------#

#------------------------------#
# Function that checks if a specified item is in the character's inventory
def itemIsInInventory(inventory, itemType):
    for item in inventory:
        if item["name"] == itemType:
            return True
    return False
#------------------------------#

#------------------------------#
# Function that returns a formatted string of an integer (basically adds a zero in front of everything less than 10 (e.g. 8 becomes "08"))
def formatNumberString(num):
    if (num < 10):
        return "0" + str(num)
    else:
        return str(num)
#------------------------------#

#///////////////////////////////#
# RSA Encryption Implementation #
#///////////////////////////////#

#------------------------------#
# Function that checks to see whether a specified number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num//2 + 1):
        if (num % i == 0):
            return False
    return True
#------------------------------#

#------------------------------#
# Function that generates a prime number on a specified range
def generate_prime(min_value, max_value):
    num = random.randint(min_value, max_value)
    while not is_prime(num):
        num = random.randint(min_value, max_value)
    return num
#------------------------------#

#------------------------------#
# Function that calculates the mod inverse for use in RSA Encryption
def mod_inverse(e, phi):
    for d in range(3, phi):
        if ((d * e) % phi == 1):
            return d
    raise ValueError("does not exist")
#------------------------------#

#------------------------------#
# Function that generates an RSA keyset
def generateRSAKeyset():
    p = generate_prime(1000, 5000)
    q = generate_prime(1000, 5000)
    while (p == q):
        q = generate_prime(1000, 5000)

    n = p * q
    phi_n = (p-1) * (q-1)

    e = random.randint(3, phi_n-1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n-1)

    d = mod_inverse(e, phi_n)

    return {
        "public": e,
        "private": d,
        "primes_product": n
    }
#------------------------------#

#------------------------------#
# Funtion that encrypts a message using the RSA algorithm
def RSA_Encrypt(msg, public_key, n):
    encoded_msg = [ord(ch) for ch in msg]
    ciphertext = [pow(ch, public_key, n) for ch in encoded_msg]
    ciphertext_str = [str(num) for num in ciphertext]
    encrypted = CIPHER_SEPARATOR.join(ciphertext_str)
    return encrypted
#------------------------------#

#------------------------------#
# Function that decrypts a message using the RSA algorithm
def RSA_Decrypt(encrypted_msg, private_key, n):
    ciphertext_str = encrypted_msg.split(CIPHER_SEPARATOR)
    ciphertext = [int(piece) for piece in ciphertext_str]
    message_characters = [pow(ch, private_key, n) for ch in ciphertext]
    decrypted = "".join(chr(ch) for ch in message_characters)
    return decrypted
#------------------------------#