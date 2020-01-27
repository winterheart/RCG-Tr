# This file is part of River City Girls L10n project
# Licensed under GPL-3+ License
# (c) 2020 Azamat H. Hackimov <azamat.hackimov@gmail.com>

from lib.rcg_l10n import RcgJsonKeys, RcgLanguages, RcgTranslation

rcg_file = RcgTranslation("data/RCG_LocalizationData.json")

# export
for lang in RcgLanguages:
    for item in RcgJsonKeys:
        rcg_file.save_po("translation", item, lang.value["iso_code"])

# import
for lang in RcgLanguages:
    for item in RcgJsonKeys:
        rcg_file.load_po("translation", item, lang.value["iso_code"])

# save
rcg_file.save_json("data/translation.json")