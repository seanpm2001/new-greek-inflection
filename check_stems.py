#!/usr/bin/env python3

import os.path
import re
import yaml


def _augment(stem):
    if stem.startswith("ἀ"):
        return "ἠ" + stem[1:]
    elif stem.startswith("ἁ"):
        return "ἡ" + stem[1:]
    elif stem.startswith("αἰ"):
        return "ᾐ" + stem[2:]
    elif stem.startswith("αὐ"):
        return "ηὐ" + stem[2:]
    elif stem.startswith("ἐ"):
        return "ἠ" + stem[1:]
    elif stem.startswith("ὀ"):
        return "ὠ" + stem[1:]
    elif stem.startswith("ὁ"):
        return "ὡ" + stem[1:]
    elif stem.startswith("οἰ"):
        return "ᾠ" + stem[2:]
    elif stem.startswith(("εἰ", "εὐ", "ἠ", "ἡ", "ἰ", "ἱ", "ὑ", "ὠ")):
        return stem
    else:
        return None


def augment(stem):
    return _augment(stem) or "ἐ" + stem


redup_table = str.maketrans("φθ", "πτ")


def redup(stem):
    return _augment(stem) or stem[0].translate(redup_table) + "ε" + stem


class Stems:

    root1regex = ".+$"

    @property
    def root1b(self): return self.root1
    @property
    def root1c(self): return self.root1b

    @property
    def P(self): return self.root1
    @property
    def I(self): return augment(self.root1)
    @property
    def F(self): return self.root1b + "σ"
    @property
    def FP(self): return self.root1c + "θη" + "σ"
    @property
    def A(self): return augment(self.root1b + "σ")
    @property
    def AN(self): return self.root1b + "σ"
    @property
    def AP(self): return augment(self.root1c + "θη!")
    @property
    def APN(self): return self.root1c + "θη!"
    @property
    def X(self): return redup(self.root1b + "κ")
    @property
    def XM(self): return redup(self.root1c)
    @property
    def Y(self): return redup(self.root1b + "κ")
    @property
    def YM(self): return redup(self.root1b)  # @@@ or root1c?

    def stems(self, lexeme):
        self.root1 = lexeme["root1"]
        assert re.match(self.root1regex, self.root1)

        return {
            key: getattr(self, key)
            for key in ["P", "I", "F", "FP", "A", "AN", "AP", "APN", "X", "XM", "Y", "YM"]
        }


class Stems0a(Stems):

    @property
    def root1c(self): return self.root1b + "σ"



class Stems0b(Stems):

    root1regex = ".+ζ$"

    @property
    def root1b(self): return self.root1[:-1]

    @property
    def root1c(self): return self.root1b + "σ"


class Stems1ab(Stems):

    root1regex = ".+ε$"

    @property
    def root1b(self): return self.root1[:-1] + "η"


class Stems1c(Stems):

    root1regex = ".+ε$"

    @property
    def root1c(self): return self.root1b + "σ"


class Stems2a(Stems):

    root1regex = ".+α$"

    @property
    def root1b(self): return self.root1[:-1] + "η"


class Stems2b(Stems):

    root1regex = ".+α$"

    @property
    def root1c(self): return self.root1 + "σ"


class Stems2c(Stems):

    root1regex = ".+α$"


class Stems3a(Stems):

    root1regex = ".+ο$"

    @property
    def root1b(self): return self.root1[:-1] + "ω"


file_list = [
    "lexicon0a.yaml",
    "lexicon0b.yaml",
    "lexicon1a.yaml",
    "lexicon1b.yaml",
    "lexicon1c.yaml",
    "lexicon2a.yaml",
    "lexicon2b.yaml",
    "lexicon2c.yaml",
    "lexicon3a.yaml",
]


for filename in file_list:
    with open(os.path.join("lexica", filename)) as f:
        for lemma, lexeme in yaml.load(f).items():
            if "prefix" in lexeme:
                continue

            assert "root1" in lexeme, lemma

            if filename in ["lexicon0a.yaml"]:
                stems = Stems0a().stems(lexeme)
            elif filename in ["lexicon0b.yaml"]:
                stems = Stems0b().stems(lexeme)
            elif filename in ["lexicon1a.yaml", "lexicon1b.yaml"]:
                stems = Stems1ab().stems(lexeme)
            elif filename in ["lexicon1c.yaml"]:
                stems = Stems1c().stems(lexeme)
            elif filename in ["lexicon2a.yaml"]:
                stems = Stems2a().stems(lexeme)
            elif filename in ["lexicon2b.yaml"]:
                stems = Stems2b().stems(lexeme)
            elif filename in ["lexicon2c.yaml"]:
                stems = Stems2c().stems(lexeme)
            elif filename in ["lexicon3a.yaml"]:
                stems = Stems3a().stems(lexeme)
            else:
                raise Exception()

            for key in stems:
                if key in lexeme:
                    assert lexeme[key] == stems[key], (lemma, key, stems[key], lexeme[key])
