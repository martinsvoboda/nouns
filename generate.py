
import os


# download and unpack treebanks from https://universaldependencies.org/#download
TREEBANKS_DIR = os.path.abspath('./ud-treebanks-v2.3/')
NOUNS_DIR = os.path.abspath('./nouns')


def get_treebanks_per_lang(dir):
    # treebanks_per_lang
    # {'cs': ['filepath', 'filepath'], 'en': [...], ...}

    treebanks_per_lang = {}

    for root, dirs, files in os.walk(dir):

        files = [p for p in files if p.endswith('-train.conllu')]

        for name in files:
            language_code = name.split('_')[0]

            file_path = os.path.join(root, name)

            treebanks_per_lang.setdefault(language_code, list())
            treebanks_per_lang[language_code].append(file_path)

    return treebanks_per_lang


def get_nouns(conllu_filepaths):
    nouns = set()

    for path in conllu_filepaths:
        with open(path) as f:
            for line in f.readlines():
                if not line[0].isdigit():
                    continue

                columns = line.split('\t')

                lemma = columns[2]
                pos_tag = columns[3]

                if pos_tag != 'NOUN':
                    continue

                nouns.add(lemma)
    return nouns


def nouns_to_file(output_dir, language_code, nouns):
    path = os.path.join(output_dir, language_code + '_nouns.txt')
    with open(path, 'w') as f:
        for noun in nouns:
            f.write(noun + os.linesep)


if __name__ == '__main__':
    treebanks = get_treebanks_per_lang(TREEBANKS_DIR)

    for language_code, filepaths in treebanks.items():
        print('Processing', language_code, '({} conllu files)'.format(len(filepaths)))
        nouns = get_nouns(filepaths)

        nouns_to_file(NOUNS_DIR, language_code, nouns)







# conllu_path = '/Users/martin.svoboda/Downloads/ud/ud-treebanks-v2.3/UD_Czech-PDT/cs_pdt-ud-train.conllu'
#
#
# nouns = set()
#
# with open(conllu_path) as f:
#     for line in f.readlines():
#         if not line[0].isdigit():
#             continue
#
# # """
# # | ID | Sentence segmentation and (surface) tokenization was automatically done and then hand-corrected; see [PDT documentation](http://ufal.mff.cuni.cz/pdt2.0/doc/pdt-guide/en/html/ch02.html). Splitting of fused tokens into syntactic words was done automatically during PDT-to-UD conversion. |
# # | FORM | Identical to Prague Dependency Treebank 3.0 form. |
# # | LEMMA | Manual selection from possibilities provided by morphological analysis: two annotators and then an arbiter. PDT-to-UD conversion stripped from lemmas the ID numbers distinguishing homonyms, semantic tags and comments; this information is preserved as attributes in the MISC column. |
# # | UPOSTAG | Converted automatically from XPOSTAG (via [Interset](https://ufal.mff.cuni.cz/interset)), from the semantic tags in PDT lemma, and occasionally from other information available in the treebank; human checking of patterns revealed by automatic consistency tests. |
# # | XPOSTAG | Manual selection from possibilities provided by morphological analysis: two annotators and then an arbiter. |
# # | FEATS | Converted automatically from XPOSTAG (via Interset), from the semantic tags in PDT lemma, and occasionally from other information available in the treebank; human checking of patterns revealed by automatic consistency tests. |
# # | HEAD | Original PDT annotation is manual, done by two independent annotators and then an arbiter. Automatic conversion to UD; human checking of patterns revealed by automatic consistency tests. |
# # | DEPREL | Original PDT annotation is manual, done by two independent annotators and then an arbiter. Automatic conversion to UD; human checking of patterns revealed by automatic consistency tests. |
# # | DEPS | &mdash; (currently unused) |
# # | MISC | Information about token spacing taken from PDT annotation. Lemma / word sense IDs, semantic tags and comments on meaning moved here from the PDT lemma. |
# # """
#
#         columns = line.split('\t')
#
#         word = columns[1]
#         lemma = columns[2]
#         pos_tag = columns[3]
#
#         if pos_tag != 'NOUN':
#             continue
#
#         nouns.add(lemma)
#
#         # print(word, lemma, pos_tag)
#
# print(len(nouns))
# print(nouns)