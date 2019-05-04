from normalize_tokens import normalize_line
import json

IN_PATH = '/Users/ruoyi/Projects/PycharmProjects/data_fixer/bash/test.cm.filtered'
OUT_PATH = '/Users/ruoyi/Projects/PycharmProjects/data_fixer/bash/test.cm.filtered.tokens'

READBACK_PATH = '/Users/ruoyi/Projects/PycharmProjects/data_fixer/bash/test.cm.filtered.readback'

if __name__ == '__main__':
    with open(IN_PATH) as in_f:
        all_tokens = []
        for l in in_f:
            try:
                tokens = normalize_line(l)
            except:
                tokens = []
            all_tokens.append(tokens)

    with open(OUT_PATH, 'w') as out_f:
        for tokens in all_tokens:
            out_f.write(json.dumps(tokens))
            out_f.write('\n')

    with open(READBACK_PATH, 'w') as rb_f:
        for tokens in all_tokens:
            rb_f.write(''.join(tokens))
            rb_f.write('\n')
