
import os

# download and unpack treebanks from https://universaldependencies.org/#download

TREEBANKS_VERSION = 'v2.10'
TREEBANKS_DIR = os.path.abspath(f'./ud-treebanks-{TREEBANKS_VERSION}/')
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
                if len(columns) < 6:
                    continue

                lemma = columns[2]
                pos_tag = columns[3]
                flags = columns[5]

                if pos_tag != 'NOUN':
                    continue

                ignore_flags = (
                    'Foreign=Yes',  # ignore foreign words
                    'Abbr=Yes',  # remove abbreviations
                    'Hyph=Yes',  # remove DE words with ending with hyph
                )

                if any(flag in flags for flag in ignore_flags):
                    continue

                # skip lemmas with non-alpha characters on begging or end
                if not lemma[0].isalpha() or not lemma[-1].isalpha():
                    continue

                nouns.add(lemma)
    return sorted(nouns)


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
