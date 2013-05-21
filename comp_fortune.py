def read_fortune(path):
    '''this open a fortune file, NOT the .dat version'''
    with open(path) as f:
        current = []
        for line in f:
            if line == '%\n':
                yield '\n'.join(current)
                current = []
            else:
                current.append(line.strip())
        if current:
            yield '\n'.join(current)

