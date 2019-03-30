# https://docs.microsoft.com/en-us/typography/opentype/spec/ttochap1

# def verify_checksum(data, checksum):
#     acc = 0
#     print(len(data) + 3, len(data) / 4)


with open('Cirka-Light.otf', 'rb') as f:
    data = f.read()

full_data = data

# CHECK 01: the first 4 bytes are otto
otto, data = data[:4], data[4:]
if otto.hex() == b'OTTO'.hex() or otto.hex() == '00010000':
    sfntVersion = otto.hex()
    print('sfntVersion:\t', sfntVersion)
else:
    print('ERROR 01: The first four bytes are', otto)
    exit()

# CHECK 02: Number of tables
numTables, data = int.from_bytes(data[:2], 'big'), data[2:]
print('numTables:\t', numTables)

# CHECK 03: Search Range
searchRange, data = int.from_bytes(data[:2], 'big'), data[2:]
print('searchRange:\t', searchRange)

# CHECK 04: Search Range
entrySelector, data = int.from_bytes(data[:2], 'big'), data[2:]
print('entrySelector:\t', entrySelector)

# CHECK 04: Range Shift
rangeShift, data = int.from_bytes(data[:2], 'big'), data[2:]
print('rangeShift:\t', rangeShift)

tables = dict()
for i in range(numTables):
    table_info = dict()
    # CHECK 05: Table tag
    tableTag, data = data[:4], data[4:]
    table_info['tag'] = tableTag
    print('table', str(tableTag))

    # CHECK 06: Checksum
    checksum, data = int.from_bytes(data[:4], 'big'), data[4:]
    table_info['checksum'] = checksum
    print('\tchecksum:\t', checksum)

    # CHECK 07: offset
    offset, data = int.from_bytes(data[:4], 'big'), data[4:]
    table_info['offset'] = offset
    print('\toffset:\t\t', offset)
    
    # CHECK 08: length
    length, data = int.from_bytes(data[:4], 'big'), data[4:]
    table_info['length'] = length
    print('\tlength:\t\t', length)

    # # CHECK 09: verify checksum
    # verify_checksum(full_data[offset:offset + length], checksum)

    tables[tableTag] = table_info
    print()

# Check the cmap table
cmap = tables['cmap']
cmap_data = full_data[cmap['offset'], cmap['length']]

# CHECK 10: cmap version

