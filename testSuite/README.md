Test Suite
==========

This directory contains a Python program checking validity of this project. It will exam that the directory layout and data is structured and formatted correctly, naming conventions are followed, no redundant duplicate data, all required fields are supplied.


Usage
-----
This program accept one optional argument specifying the directory. If the argument is not provided, it will check all directory `../allergens` `../cuisines` `../diets` `../ingredients`.

__Example:__

```Bash
$ python3 testSuites.py
$ python3 testSuites.py ../allergens
```


Dependences
-----------
[__TOML 0.9.3__](https://github.com/uiri/toml)

A Python library for parsing and creating TOML.


General Test Cases
------------------
* Filenames should contain only lowercase letters (a-z) numbers, dots and hyphens `[a-z0-9.-]`
* Attributes should only contain lowercase letters (a-z) numbers and hyphens `[a-z0-9-]`. Excludes attributes within a translation attribute (see translation case).
* If a folder exists inside there must be a file with the same name (in the same level). Excludes folders that have the prefix `__`.


Translation Test Cases
----------------------

* Attributes inside a `translation` should follow this format. For the first level, the current level attribute should be 2 lowercase letters (a-z). For the second level, the current level attribute should be 2 uppercase letters (A-Z). For the third level, the current level attribute should be 3 uppercase letters (A-Z). The following are valid translation attributes: `translation.aa`, `translation.aa.BB`, `translation.aa.BB.CCC`. The following are invalid translation attributes: `translation.AA`, `translation.aa.bb.CCC`, `translation.aaa`, `translation.aa.BBB`, `translation.aa.BB.CC`.
* If they have a value, it should be a lowercase string (any character is valid).


Ingredients Test Cases
----------------------
* The `exclude-diet` field should have a list of strings as its value (may be an empty list). These strings should reference the filenames of diets that exists in `diets/`.
* The `exclude-allergen` field should have a list of strings as its value (may be an empty list). These strings should reference the filenames of allergens that exists in `allergens/`.


Cuisines Test Cases
-------------------

* Cuisines must have a `type` field, with a value of "continent", "subregion", "country", "province", "culture" or "other".
* If cuisines have a `cuisine` attribute, it should be of the format `cuisine.<name>.translation`, where `name` is a custom name. The translation portion falls under the same rules as the translation attribute.
