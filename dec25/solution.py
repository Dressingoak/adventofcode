enc = list()

for line in open("input.txt").read().strip().split("\n"):
    pub = int(line)
    print("[DEBUG] Public key is {}".format(pub))
    value = 1
    subject = 7
    size = 0
    while True:
        value *= subject
        value %= 20201227
        size += 1
        if value == pub:
            break
    enc.append((pub, size))
    print("[DEBUG] Loop size for public key {} is {}".format(pub, size))

if len(enc) != 2:
    raise Exception("Unexpected number of keys: {}".format(len(enc)))

enc_key = None
for i in range(2):
    value = 1
    subject = enc[i][0]
    size = enc[(i+1)%2][1]
    print("[DEBUG] Using public key {} and loops {}".format(subject, size))
    for j in range(size):
        value *= subject
        value %= 20201227
    if enc_key is None:
        enc_key = value
    if enc_key is not None:
        if enc_key != value:
            raise Exception("Didn't find correct encryption key (was {}, but got {} previously)".format(value, enc_key))

print("Part 1: {}".format(enc_key))
