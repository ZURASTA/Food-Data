# A test suite in Python 3 checking validity of Food-Data

import toml
import re
from pathlib import Path
import sys


# main will return 0 if no exception raises
# main will return -1 if any exception raises
returnVal = 0


# A valid filename should only contain lowercase letters
# and hyphens
def validFilename(filename):
    result = re.findall('[^a-z\-\.]', filename)
    if not len(result) == 0:
        raise configError('invalid filename')


# A valid attribute should only contain lowercase letters,
# hyphens and numbers, except attributes under translation
def validAttribute(attribute):
    result = re.findall('[^a-z1-9\-]', attribute)
    if not len(result) == 0:
        raise configError('invalid attribute')


# A valid value should only contain lowercase letters (any
# characters in different languages)
def validValue(value):
    for character in value:
        if character.isupper():
            raise configError('invalid value: "' + value + '" (must be lowercase)')


# Traverse a dictionary parsed from a .toml file with many
# layers to exam the validation for attribute names and
# values on each layer
def traverseDictionary(element):
    if type(element) == str:
        validValue(element)
    elif type(element) == dict:
        # traverse items
        for item in element.items():
            key = item[0]
            value = item[1]
            validAttribute(key)

            # apply different validation rules based on key
            if key == 'translation':
                validTranslation(value, 1)
            elif key == 'exclude-diet':
                validExDiet(value)
            elif key == 'exclude-allergen':
                validExAllergen(value)
            elif key == 'type':
                validCuisineType(value)
            else:
                traverseDictionary(value)


# A vaild translation dictionary can have three levels:
#  - The first level should be 2 lowercase letters
#  - The second level should be 2 uppercase letters
#  - The third level should be 1 to 3 uppercase letters
def validTranslation(dictionary, level):
    # verify data type of argument
    if not type(dictionary) == dict:
        raise configError('invalid translation')

    # declare naming pattern for certain layer
    lowest = False
    match = ''
    error = ''
    if level == 1:
        match = '[a-z]{2}'
        error = 'must be lowercase 2 letter language code [ISO 639-1]'
    elif level == 2:
        match = '[A-Z]{2}'
        error = 'must be uppercase 3 letter country code [ISO 3166-1 alpha-2]'
    elif level == 3:
        match = '[A-Z]{1,3}'
        error = 'must be uppercase 1 - 3 letter subdivision code [ISO 3166-2]'
    elif level == 4:
        lowest = True
    else:
        raise configError('invalid translation')

    if not lowest:
        for item in dictionary.items():
            key = item[0]
            val = item[1]
            if type(val) == str:
                validValue(val)
            elif type(val) == dict:
                result = re.fullmatch(match, key)
                if result == None:
                    raise configError('invalid translation: "' + key + '" (' + error + ')')
                validTranslation(val, level + 1)
    else:
        for item in dictionary.items():
            key = item[0]
            val = item[1]
            if type(val) == str:
                validValue(val)
                validAttribute(key)
            else:
                raise configError('invalid translation')


# The value shoud be one of `"continent", "subregion", "country",
# "province" or "culture".
def validCuisineType(value):
    if type(value) == str:
        if (value == 'continent'
        or value == 'subregion'
        or value == 'country'
        or value == 'province'
        or value == 'culture'
        or value == 'dish'
        or value == 'other'):
            return
    raise configError('invalid cuisine type')


# should have a list of strings as its value (may be an empty
# list). These strings should reference the filenames of diets
# that exists in diets/
def validExDiet(value):
    # get the path to diets/
    path = Path('./diets')
    # exam the reference
    if type(value) == list:
        for ele in value:
            filename = ele + '.toml'
            pathToFile = path / filename
            if not pathToFile.is_file():
                raise configError('invalid exclude-diet')
    else:
        raise configError('invalid exclude-diet')


# should have a list of strings as its value (may be an empty
# list). These strings should reference the filenames of allergens
# that exists in allergens/
def validExAllergen(value):
    # get the path to allergens/
    path = Path('./allergens')
    # exam the reference
    if type(value) == list:
        for ele in value:
            filename = ele + '.toml'
            pathToFile = path / filename
            if not pathToFile.is_file():
                raise configError('invalid exclude-allergen')
    else:
        raise configError('invalid exclude-allergen')


# A cuisine must have a type attribute
def cuisineTypeExist(path, dictionary):
    if ('cuisines' in path.parts
    and not 'type' in dictionary.keys()):
        raise configError('invalid cuisines')


# If a folder exists inside there must be a file with the
# same name (in the same level).
# Excludes folders that have the prefix __
def validDirectory(folder):
    path = Path(folder)
    for child in path.iterdir():
        if child.is_dir() and child.stem[:2] != '__':
            filename = child.with_suffix('.toml')
            if not filename.is_file():
                raise configError('invalid folder')


# Parse a .toml file into a dictionary and exam its validation
def validFile(folder):
    # get global variable returnVal
    global returnVal

    # exam the validation of the folder structure
    try:
        validDirectory(folder)
    except configError as e:
        returnVal = -1
        print(e.message, 'in\n', folder)
    except Exception as e:
        returnVal = -1
        print(e)

    # read .toml in the folder
    path = Path(folder)
    tomlFileList = list(path.glob('*.toml'))
    for f in tomlFileList:
        try:
            # exam the validation of filename
            validFilename(f.stem)

            # parse .toml file into a dictionary and traverse it
            fs = f.open()
            tomlString = fs.read()
            fs.close()
            parsedData = toml.loads(tomlString)
            cuisineTypeExist(f, parsedData)
            traverseDictionary(parsedData)
        except configError as e:
            returnVal = -1
            print(e.message, 'in\n', f)
        except Exception as e:
            returnVal = -1
            print(e)

    # traverse sub-folder
    for child in path.iterdir():
        if child.is_dir() and child.stem[:2] != '__':
            validFile(child)

# A exception class with a message
class configError(Exception):
    def __init__(self, message):
        self.message = message


# entrance function
def main():
    if len(sys.argv) == 2:
        print('Test: ', sys.argv[1])
        validFile(sys.argv[1])
    elif len(sys.argv) == 1:
        print('Test all folders')
        validFile('./cuisines')
        validFile('./diets')
        validFile('./ingredients')
        validFile('./allergens')
    else:
        print('Wrong arguments')
    sys.exit(returnVal)

if __name__ == '__main__':
    main()
