import re
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("""CREATE TABLE data (
    byr TEXT,
    iyr TEXT,
    eyr TEXT,
    hgt TEXT,
    hcl TEXT,
    ecl TEXT,
    pid TEXT,
    cid TEXT
)""")

input_data = list(map(lambda x: re.split(r'\s+|\n+', x), "".join(open("input.txt").readlines()).split('\n\n')))

def entry_to_dict(entry):
    return {e.split(":")[0]: e.split(":")[1] for e in entry if e}

for entry in input_data:
    d = entry_to_dict(entry)
    sql = "INSERT INTO data ({}) VALUES ({})".format(", ".join(d.keys()), ", ".join(["?"] * len(d)))
    conn.execute(sql, [_ for _ in d.values()])

(result1, ) = conn.execute("""
SELECT 
    COUNT(*)
FROM data
WHERE 
    byr IS NOT NULL AND
    iyr IS NOT NULL AND
    eyr IS NOT NULL AND
    hgt IS NOT NULL AND
    hcl IS NOT NULL AND
    ecl IS NOT NULL AND
    pid IS NOT NULL
""").fetchone()
print("Part 1: {}".format(result1))

def validate_byr(byr):
    m = re.match(r'^(\d{4})$', str(byr))
    if m:
        value = int(m.group(1))
        if value < 1920 or value > 2002:
            return False
        else:
            return True
    else:
        return False

def validate_iyr(iyr):
    m = re.match(r'^(\d{4})$', str(iyr))
    if m:
        value = int(m.group(1))
        if value < 2010 or value > 2020:
            return False
        else:
            return True
    else:
        return False

def validate_eyr(eyr):
    m = re.match(r'^(\d{4})$', str(eyr))
    if m:
        value = int(m.group(1))
        if value < 2020 or value > 2030:
            return False
        else:
            return True
    else:
        return False

def validate_hgt(hgt):
    m = re.match(r'^(\d+)(cm|in)$', str(hgt))
    if m:
        value = int(m.group(1))
        unit = m.group(2)
        if unit == "cm":
            if value < 150 or value > 193:
                return False
            else:
                return True
        else:
            if value < 59 or value > 76:
                return False
            else:
                return True
    else:
        return False

def validate_hcl(hcl):
    m = re.match(r'^#[0-9a-f]{6}$', str(hcl))
    if m:
        return True
    else:
        return False

def validate_ecl(ecl):
    m = re.match(r'^(amb|blu|brn|gry|grn|hzl|oth)$', str(ecl))
    if m:
        return True
    else:
        return False

def validate_pid(pid):
    m = re.match(r'^([0-9]{9})$', str(pid))
    if m:
        return True
    else:
        return False

sqlite3.enable_callback_tracebacks(True)
conn.create_function("validate_byr", 1, validate_byr)
conn.create_function("validate_iyr", 1, validate_iyr)
conn.create_function("validate_eyr", 1, validate_eyr)
conn.create_function("validate_hgt", 1, validate_hgt)
conn.create_function("validate_hcl", 1, validate_hcl)
conn.create_function("validate_ecl", 1, validate_ecl)
conn.create_function("validate_pid", 1, validate_pid)

(result2, ) = conn.execute("""
SELECT 
    COUNT(*)
FROM data
WHERE 
    validate_byr(byr) AND
    validate_iyr(iyr) AND
    validate_eyr(eyr) AND
    validate_hgt(hgt) AND
    validate_hcl(hcl) AND
    validate_ecl(ecl) AND
    validate_pid(pid)
""").fetchone()
print("Part 2: {}".format(result2))
