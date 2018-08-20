Ingredients
===========

This directory contains ingredient related data. Organised by grouping ingredients to different culinary groups, and associating different data with those.

Structure
---------

The data is organised into TOML files per ingredient or ingredient/culinary type. Where attributes specified in parent folders applies to all children in that folder.

An example of this structure:

```
ingredients/
├── meats.toml #contains info that is applied to all meats
├── meats/
│   └── pork.toml #contains info that is applied to pork and inherits the attributes applied to meats
├── vegetables.toml #contains info that is applied to all vegetables
└── vegetables/
    ├── spring-onion.toml #contains info that is applied to spring-onion and inherits the attributes applied to vegetables
    ├── tubers.toml #contains info that is applied to tubers and inherits the attributes applied to vegetables
    └── tubers/
        └── potato.toml #contains info that is applied to potato and inherits the attributes applied to vegetables and tubers
```


Data
----

The TOML file itself contains attributes that should be applied to that ingredient/groups and attributes that should also be applied any child ingredients/groups.

The current list of attributes that are applied to the object itself:

* __translation__ - The current translations for the given item.

The current list of attributes that are applied to the object and child objects:

* __exclude-diet__ - The diets that do not allow consumption of this ingredient or type of ingredient. By default all diets are allowed to consume the ingredient unless specifically excluded.

* __exclude-allergen__ - The allergies that are triggered by consumption of this ingredient or type of ingredient. By default all allergy types are allowed to consume the ingredient unless specifically excluded.


An example of this is (meats.toml):

```toml
# https://en.wikipedia.org/wiki/Meat
exclude-diet = ["vegan", "vegetarian", "pescetarian", "raw-vegan", "fruitarian"]

[translation]
  [translation.en]
    term = "meat"
  [translation.fr]
    term = "viande"
```

The above indicates that a meat (or `meats`) and any items in that category (in the `meats/` directory) are excluded from vegan, vegetarian, pescetarian, raw-vegan and fruitarian diets. Translations for meat have also been provided in the english and french. For more information on how translations work see: [translations.md](../translations.md).


Processed Ingredients
---------------------

For the sake of simplicity, any ingredients that are prepared/processed (either from an individual or combination of ingredients), will not include `exclude-diet`, `exclude-allergen` information. Since for many of these ingredients, there's often different variants to suit people with different dietary requirements.
