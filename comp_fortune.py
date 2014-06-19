def read_fortune(path):
    '''this open a fortune file, NOT the .dat version'''
    with open(path) as f:
        current = []
        for line in f:
            line = line.decode('utf-8')
            if line == '%\n':
                yield '\n'.join(current)
                current = []
            else:
                current.append(line.strip())
        if current:
            yield '\n'.join(current)

def add_fortune(path, quote, verify=False):
    quote = quote.strip()
    if verify:
        try:
            if quote in read_fortune(path):
                return
        except IOError:
            pass

    with open(path, 'a') as f:
        f.write('%s\n%%\n' % quote.strip().encode('utf-8'))
