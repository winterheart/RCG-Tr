# This file is part of River City Girls L10n project
# Licensed under GPL-3+ License
# (c) 2020 Azamat H. Hackimov <azamat.hackimov@gmail.com>

from datetime import datetime
from enum import Enum
import logging
from os import makedirs
from os.path import join, exists
from polib import POEntry, POFile, pofile
from simplejson import OrderedDict
import simplejson as json


class RcgJsonKeys(Enum):
    # Some constants from JSON dictionary
    NON_DIALOG_KEYS = "Non_Dialog_Keys"
    USEABLES_KEYS = "Useables_Keys"
    MOVE_KEYS = "Move_Keys"
    QUEST_KEYS = "Quest_Keys"
    QUESTITEM_KEYS = "QuestItem_Keys"
    EQUIP_KEYS = "Equip_Keys"
    STORE_KEYS = "Store_Keys"
    DIALOG_KEYS = "Dialog_Keys"
    TUTORIAL_KEYS = "Tutorial_Keys"
    METADATA_KEYS = "MetaData_Keys"


class RcgLanguages(Enum):
    LANG_ENGLISH = {"key": "English", "iso_code": "en"}
    LANG_FRENCH = {"key": "French", "iso_code": "fr"}
    LANG_GERMAN = {"key": "German", "iso_code": "de"}
    LANG_ITALIAN = {"key": "Italian", "iso_code": "it"}
    LANG_SPANISH = {"key": "Spanish", "iso_code": "es"}
    LANG_JAPANESE = {"key": "Japanese", "iso_code": "ja"}
    LANG_KOREAN = {"key": "Korean", "iso_code": "ko"}
    LANG_CHINESESIMPLIFIED = {"key": "ChineseSimplified", "iso_code": "zh-cn"}
    LANG_CHINESETRADITIONAL = {"key": "ChineseTraditional", "iso_code": "zh-tw"}
    LANG_RUSSIAN = {"key": "Russian", "iso_code": "ru"}


LANG_KEY = "Key"

METADATA_ENTRY = {
    'Project-Id-Version': '1.0',
    'Report-Msgid-Bugs-To': 'you@example.com',
    'POT-Creation-Date': datetime.now().isoformat(" "),
    'PO-Revision-Date': datetime.now().isoformat(" "),
    'Last-Translator': 'you <you@example.com>',
    'Language-Team': '',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
}


class RcgTranslation:
    def __init__(self, json_path):
        """
        Init class for handling RCG_LocalizationData.json
        :param json_path: Path to JSON file (UTF-8 with BOM)
        """
        with open(json_path, "r", encoding="utf-8-sig") as read_file:
            self.json_content = json.load(read_file)
            # Make entries unique
            for key in RcgJsonKeys:
                self.json_content[key.value] = list({v[LANG_KEY]: v for v in self.json_content[key.value]}.values())

    def save_json(self, json_path):
        """
        Save class as complete RCG_LocalizationData.json file
        :param json_path: path to JSON file
        :return:
        """
        with open(json_path, "w", encoding="utf-8-sig", newline="\r\n") as write_file:
            json.dump(self.json_content, write_file, ensure_ascii=False, indent=2)
        return

    def generate_pot(self, json_root_key):
        """
        Generate and return POT file object
        :param json_root_key: JSON key from RcgJsonKeys class
        :return: POT file object
        """
        pot = POFile(check_for_duplicates=True)
        pot.metadata = METADATA_ENTRY
        pot.metadata_is_fuzzy = 1

        for entry in self.json_content[json_root_key.value]:
            if entry[RcgLanguages.LANG_ENGLISH.value["key"]] != "":
                po_entry = POEntry(
                    msgctxt=entry[LANG_KEY],
                    msgid=entry[RcgLanguages.LANG_ENGLISH.value["key"]],
                )
                try:
                    pot.append(po_entry)
                except ValueError:
                    logging.debug("Entry {} already exists, skipping...".format(entry[LANG_KEY]))

        return pot

    def save_pot(self, path, json_root_key):
        """
        Save Gettext POT file from JSON root key into path
        :param path: Directory path save to
        :param json_root_key: JSON key from RcgJsonKeys class
        :return:
        """
        pot = self.generate_pot(json_root_key)
        if not exists(path):
            makedirs(path)
        pot.save(join(path, json_root_key.value + ".pot"))

        return

    def load_po(self, path, json_root_key, lang):
        """
        Load content of Gettext PO file (from "path/lang/json_root_key.po") into already loaded JSON content
        :param path: Root directory
        :param json_root_key: JSON key from RcgJsonKeys class
        :param lang: Language. Should be in RcgLanguages class
        :return:
        """

        if len(self.json_content[json_root_key.value]) == 0:
            logging.error("ERROR: {} JSON entry is empty! Forgot to load_json()?".format(json_root_key.value))
            return

        temp_json = OrderedDict([])
        temp_json.update({json_root_key.value: []})

        language = next(name.value["key"] for name in RcgLanguages if name.value["iso_code"] == lang)

        po_file = join(path, lang, json_root_key.value + ".po")

        if exists(po_file):
            po = pofile(po_file)

            for entry in po:
                json_entry = next(
                    item for item in self.json_content[json_root_key.value] if item[LANG_KEY] == entry.msgctxt)
                if not entry.obsolete and entry.translated() and "fuzzy" not in entry.flags:
                    json_entry[language] = entry.msgstr
                # else:
                    # FIXME Don't overwrite?
                    # json_entry[language] = entry.msgid
        else:
            logging.warning("ERROR: '{}' is not exists! Skipping.".format(po_file))

        return

    def save_po(self, path, json_root_key, lang):
        """
        Save Gettext PO file into directory structure as "path/lang/json_root_key.po"
        If "path/lang/json_root_key.po" already exists, it will be updated accordingly to JSON dict
        :param path: Root directory where place to files
        :param json_root_key: JSON key from RcgJsonKeys class
        :param lang: Language to translate. Should be in RcgLanguages class
        :return:
        """
        language = next(name for name in RcgLanguages if name.value["iso_code"] == lang)
        save_path = join(path, lang)
        save_file = join(save_path, json_root_key.value + ".po")

        if not exists(save_path):
            makedirs(save_path)
        if exists(save_file):
            # File already exists, let's try to update it
            logging.info("Updating '{}'...".format(save_file))
            po = pofile(save_file)
            pot = self.generate_pot(json_root_key)
            po.merge(pot)
            po.save(save_file)
        else:
            # File does not exists, create it from JSON data
            logging.info("Creating '{}'...".format(save_file))
            po = POFile(check_for_duplicates=True)
            po.metadata = METADATA_ENTRY

            for entry in self.json_content[json_root_key.value]:
                if entry[RcgLanguages.LANG_ENGLISH.value["key"]] != "":
                    po_entry = POEntry(
                        msgctxt=entry[LANG_KEY],
                        msgid=entry[RcgLanguages.LANG_ENGLISH.value["key"]],
                    )
                    if language.value["key"] in entry and entry[language.value["key"]] is not None:
                        po_entry.msgstr = entry[language.value["key"]]
                        po_entry.flags.append("fuzzy")
                    try:
                        po.append(po_entry)
                    except ValueError:
                        logging.debug("Entry {} already exists, skipping...".format(entry[LANG_KEY]))

            po.save(save_file)

        return
