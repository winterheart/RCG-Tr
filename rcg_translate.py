# This file is part of River City Girls L10n project
# Licensed under GPL-3+ License
# (c) 2020 Azamat H. Hackimov <azamat.hackimov@gmail.com>

import json
from lib.rcg_l10n import RcgJsonKeys, RcgLanguages, RcgTranslation

#rcg_file = RcgTranslation()
#rcg_file.load_json("data/RCG_LocalizationData.json")
#rcg_file.load_po("translation", RcgJsonKeys.NON_DIALOG_KEYS, RcgLanguages.LANG_RUSSIAN.value["iso_code"])
#rcg_file.save_json("data/translation.json")

rcg_file = RcgTranslation("data/RCG_LocalizationData.json")
for item in RcgJsonKeys:
    rcg_file.save_pot("translation", item)

#for item in RcgJsonKeys:
#    rcg_file.save_po("translation", item, "ru")
