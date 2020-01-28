#!/usr/bin/env python
# This file is part of River City Girls L10n project
# Licensed under GPL-3+ License
# (c) 2020 Azamat H. Hackimov <azamat.hackimov@gmail.com>

"""
RCG Translate - translation tool for River City Girls text resources

Usage:
    rcg_translate extract --input=<input_json> --podir=<podir> [--lang=<language>...] [-V]
    rcg_translate pack --input=<input_json> --podir=<podir> --output=<output_json> [--lang=<language>...] [-V]
    rcg_translate --help
    rcg_translate --version

Commands:
    extract     Extract text resources from RCG_LocalizationData.json into Gettext PO files
    pack        Create updated JSON file based on RCG_LocalizationData.json and Gettext PO files

Options:
    -i IN_JSON --input=IN_JSON      Source RCG_LocalizationData.json file
                                    This file located in <ROOT>/RiverCityGirls_Data/StreamingAssets/LocalizationData
    -p PO_DIR --podir=PO_DIR        Directory where Gettext PO files will be placed or fetched
    -l LANG --lang=LANG             Process only specified language. This parameter can be defined multiple times
                                    By default will be processed all supported languages
    -o OUT_JSON --output=OUT_JSON   Path to translated RCG_LocalizationData.json
    -V --verbose                    Enable verbose output
    -h --help                       Print this help
    -v --version                    Print version and exit

Description:
RCG Translate tool

Copyright:
    (c) 2020 Azamat H. Hackimov <azamat.hackimov@gmail.com>
    License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it. There is NO WARRANTY,
    to the extent permitted by law.

"""

import logging
from docopt import docopt
from lib.rcg_l10n import RcgJsonKeys, RcgLanguages, RcgTranslation
from os.path import exists

version = "RCG Translate 0.5"

if __name__ == "__main__":
    args = docopt(__doc__, version=version)

    logger = logging.getLogger("RCG")
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(name)s: %(message)s')
    if args["--verbose"]:
        logger.setLevel(logging.INFO)

    if not exists(args["--input"]):
        logger.error("'{}' does not exist! Please specify correct path.".format(args["--input"]))
        exit(-2)

    languages = []
    # Validate languages
    if len(args["--lang"]):
        for lang in args["--lang"]:
            try:
                language = next(name.value["iso_code"] for name in RcgLanguages if name.value["iso_code"] == lang)
                languages.append(language)
            except StopIteration:
                logger.warning("{} is not supported, skipping it.".format(lang))

    if len(languages) == 0:
        for lang in RcgLanguages:
            languages.append(lang.value["iso_code"])
    logger.info("Processing languages: {}".format(languages))

    if args["extract"]:
        logger.info("Extracting text data into {}".format(args["--podir"]))
        rcg_translation = RcgTranslation(args["--input"])

        for lang in languages:
            for item in RcgJsonKeys:
                rcg_translation.save_po(args["--podir"], item, lang)
        logger.info("Done!")

    if args["pack"]:
        logger.info("Packing text data into {}".format(args["--output"]))
        rcg_translation = RcgTranslation(args["--input"])

        for lang in languages:
            for item in RcgJsonKeys:
                rcg_translation.load_po(args["--podir"], item, lang)

        rcg_translation.save_json(args["--output"])
        logger.info("Done!")
