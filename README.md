# RCG-Tr - River City Girls Translation tool

RCG Translate (RCG-Tr) is open-source tool written in Python that helps
to translate text from River City Girl game into various languages.

## Installation

Requirements:

* Python 3.x (tested on Python 3.6)
* [docopt>=0.6.2](https://pypi.org/project/docopt/)
* [polib>=1.1.0](https://pypi.org/project/polib/)
* [simplejson>=3.16.0](https://pypi.org/project/simplejson/)

You can install them via package manager of your system or pip:

```
pip install -r requirements.txt
```

## Structure of RCG_LocalizationData.json

`RCG_LocalizationData.json` is standard JSON file (UTF-8 with BOM,
CRLF) that contains all text messages in 10 languages. These messages
are grouped into 10 groups:

* Dialog_Keys - dialogs and replies
* Equip_Keys - info about weapons
* MetaData_Keys - messages for Achievements and various descriptions for
Steam, Xbox, PS4, Switch stores
* Move_Keys - names of attacks
* Non_Dialog_Keys - strings for UI
* Quest_Keys - main and side quests
* QuestItem_Keys - descriptions for quest items
* Store_Keys - names of in-game stores
* Tutorial_Keys - messages for tutorial
* Useables_Keys - names and descriptions for consumables and outfits

Each group is list of dictionaries that contains `Key` of message and
translated strings. Here example of that dict:
```
{
  "Key": "LBL_CHARACTER",
  "English": "Character",
  "French": "Personnage",
  "German": "Charakter",
  "Italian": "Personaggio",
  "Spanish": "Personaje",
  "Japanese": "キャラクター",
  "Korean": "캐릭터",
  "ChineseSimplified": "角色",
  "ChineseTraditional": "角色",
  "Russian": "Персонаж"
}
```
## Usage

RCG-Tr supports two commands - `extract` and `pack` - for extracting
from `RCG_LocalizationData.json` to Gettext PO files and packing them
back into modified `*.json` file.

Run `python rcg_translate.py --help` for usage.

### Extracting

`extract` command extracts dictionaries from JSON files into 10 Gettext
PO files for each supported language. If PO files already exists, RCG-Tr
tries to update them. All already translated text will be preserved.

Here some examples:

```
# Extract all messages from JSON into translation directory:
python rcg_translate.py extract extract -i RCG_LocalizationData.json -p translation
# Extract only Korean messages:
python rcg_translate.py extract extract -i RCG_LocalizationData.json -p translation -l ko
```

After extacting files will be placed into `translation/<lang>/`
directories.

### Packing

`pack` command packs translated Gettext PO files back into JSON format,
compatible with RCG. Please note, that you cannot use
`RCG_LocalizationData.json` as output file, this file is used for
reference.

Examples:

```
# Pack all messages into data.json
python rcg_translate pack --i RCG_LocalizationData.json -p translation -o data.json
# Pack only Korean message, leave other messages intact:
python rcg_translate pack --i RCG_LocalizationData.json -p translation -o data.json -l ko
```

### Gettext PO Editors

Since Gettext PO is just text file, it may be opened by any text editor
that support UTF-8 encoding like Notepad++ for Windows. But is better
to use a special editor that supports Gettext PO catalogs, like
[POEdit](https://poedit.net/) or
[Lokalize](https://userbase.kde.org/Lokalize/).

Each message in PO file can be in one of four states: obsoleted,
untranslated, translated and fuzzy. RCG-Tr uses only translated entries
during packing. If entry in non-translated state, original message will
be used (or English if there no such entry in original JSON).

## License

Copyright (c) 2020 Azamat H. Hackimov <azamat.hackimov@gmail.com>

License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
