"""Converte fórmula Power Fx invariante (en-US) para a notação pt-BR exibida no Studio."""
import re

NUM = re.compile(r'(?<![\w.])(\d+)\.(\d+)')


def to_ptbr(f):
    out, i = [], 0
    while i < len(f):
        if f[i] == '"':
            j = i + 1
            while j < len(f):
                if f[j] == '"':
                    if j + 1 < len(f) and f[j + 1] == '"':
                        j += 2
                        continue
                    break
                j += 1
            out.append(f[i:j + 1])
            i = j + 1
            continue
        k = f.find('"', i)
        k = len(f) if k < 0 else k
        code = f[i:k].replace(';', '\x00').replace(',', ';').replace('\x00', ';;')
        out.append(NUM.sub(r'\1,\2', code))
        i = k
    return ''.join(out)
