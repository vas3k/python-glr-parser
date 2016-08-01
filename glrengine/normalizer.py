# -*- coding: utf-8 -*-
import pymorphy2


class GLRNormalizer(object):
    TAG_MAPPER = {
        "NOUN": "noun",
        "ADJF": "adj",
        "ADJS": "adj",
        "COMP": "adj",
        "VERB": "verb",
        "INFN": "verb",
        "PRTF": "pr",
        "PRTS": "pr",
        "GRND": "dpr",
        "NUMR": "num",
        "ADVB": "adv",
        "NPRO": "pnoun",
        "PRED": "adv",
        "PREP": "prep",
        "CONJ": "conj",
        "PRCL": "prcl",
        "INTJ": "noun",
        "LATN": "lat",
        "NUMB": "num"
    }

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def __call__(self, tokens):
        results = []
        for token in tokens:
            tokname, tokvalue, tokpos = token
            orig_tokvalue = tokvalue
            multitag = None # multitag collects all grammemes of lemma forms
            if tokname == "word":
                morphed = self.morph.parse(tokvalue)
                for lemma in morphed:
                    if not multitag:
                        multitag = self.morph.TagClass(",".join(lemma.tag.grammemes))
                        tokvalue = lemma.normal_form
                        # TODO: make tokname an array, because word can be in multiple POS
                        # example: чёрный (сущ. / прил.)
                        tokname = self.TAG_MAPPER.get(lemma.tag.POS) or tokname
                    # tokparams = unicode(morphed[0].tag).lower().split(",")
                    multitag._grammemes_cache =  multitag.grammemes | lemma.tag.grammemes
                    multitag._str = ",".join(multitag.grammemes) # not required, but useful for debugging
            # print tokname, tokvalue, tokpos, multitag, orig_tokvalue
            results.append((tokname, tokvalue, tokpos, multitag, orig_tokvalue))
        return results

    def normal(self, word):
        morphed = self.morph.parse(word)
        if morphed:
            return morphed[0].normal_form
        return word

    def parse_tags(self, word):
        parsed = self.morph.parse(word)
        if not parsed:
            return None
        return parsed[0].tag

morph_parser = GLRNormalizer()


