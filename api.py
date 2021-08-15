"""
The following is a wrapper over https://github.com/soimort/translate-shell, the AWK-based tool for
working with Google Translator API and God only knows what else made by magnificent @Soimort
"""

import sys
from generic import command_output
import json


class Soimort:

    @staticmethod
    def _extract_json(raw_s):
        first_sb_pos = raw_s.find('[')
        last_sb_pos = raw_s.rindex(']')
        return raw_s[first_sb_pos: last_sb_pos + 1]

    @staticmethod
    def _iterate(json_s):
        """
        Iterate through json [sub]tree, extract matching subtrees
        :param self:
        :param json_s:
        :return:
        """
        results = []

        if hasattr(json_s, "__iter__") and type(json_s) is not str:
            for item in json_s:
                if Soimort._subtree_match(item):
                    results += [Soimort._subtree_extract_stringify(item)]
                results += Soimort._iterate(item)

        return results

    @staticmethod
    def _subtree_match(item):
        """
        The expected structure is something ["string": ["string", "string", "string", ...] *]
        :param item:
        :return:
        """
        if hasattr(item, "__iter__"):
            if len(item) >= 2:
                if type(item[0]) is str and type(item[1]) is list:
                    if all([type(i) is str for i in item[1]]):
                        return True
        return False


    @staticmethod
    def _subtree_extract_stringify(item):
        return item[0] + ": " + ", ".join(item[1])

    @staticmethod
    def _extract_translation_subtrees(json_s):
        json_s = Soimort._extract_json(json_s)
        json_s = json.loads(json_s)
        print(json_s)
        return Soimort._iterate([json_s])

    def translate(self, query, lang_from, lang_to):
        """
        :param query:
        :return: array-like, iterable
        """

        s, _ = command_output(f'./trans -dump -s={lang_from} -t={lang_to} "{query}"')

        # TODO: Have no time to delve into structure of the response API.
        # There is a pattern here, and we're gonna use it. The returned
        # sequence is a JSON. The JSON contains sequences like:
        #   ...  "string", ["string", "string", "string"]  ...
        # When we find a subtree of this structure, we extract it and pass it as a
        # translation (after the string is subjected to "human-enreadability" procedure)

        # Extract the json-part
        s = Soimort._extract_translation_subtrees(s)

        return s


if __name__ == "__main__":
    s = Soimort()
    print(s.translate(sys.argv[1], "en", "ru"))
