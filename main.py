# https://docs.microsoft.com/en-us/typography/opentype/spec/ttochap1

# def verify_checksum(data, checksum):
#     acc = 0
#     print(len(data) + 3, len(data) / 4)


def main(data):
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

    required_tables = {b'cmap': parse_cmap,
                       b'head': parse_head,
                       b'hhea': parse_hhea,
                       b'hmtx': parse_hmtx,
                       b'maxp': parse_maxp,
                       b'name': parse_name,
                       b'OS/2': parse_os2,
                       b'post': parse_post}
    for key in required_tables.keys():
        table_info = tables[key]
        offset, length = table_info['offset'], table_info['length']
        required_tables[key](full_data[offset:offset + length])
   

def parse_cmap(cmap_data):
    print('***** CMAP INFO *****')
    total_cmap_data = cmap_data

    # CHECK 10: cmap version
    cmap_version, cmap_data = int.from_bytes(cmap_data[:2], 'big'), cmap_data[2:]
    print('cmap version:\t\t', cmap_version)

    # CHECK 11: num_tables
    cmap_num_tables, cmap_data = int.from_bytes(cmap_data[:2], 'big'), cmap_data[2:]
    print('cmap num tables:\t', cmap_num_tables)

    cmap_tables = []
    for i in range(cmap_num_tables):
        # CHECK 12: platform id
        platform_id, cmap_data = int.from_bytes(cmap_data[:2], 'big'), cmap_data[2:]

        # CHECK 13: encoding id
        encoding_id, cmap_data = int.from_bytes(cmap_data[:2], 'big'), cmap_data[2:]
        
        # CHECK 14: offset
        offset, cmap_data = int.from_bytes(cmap_data[:4], 'big'), cmap_data[4:]

        cmap_tables.append((platform_id, encoding_id, offset))
        print('table', i, '\tplatfrm id:', platform_id, '\tencding id:', encoding_id, '\toffset:', offset)

    print()


def parse_head(head_data):
    print('***** HEAD INFO *****')
    print()


def parse_hhea(hhea_data):
    print('***** HHEA INFO *****')
    print()


def parse_hmtx(hmtx_data):
    print('***** HMTX DATA *****')
    print()


def parse_maxp(maxp_data):
    print('***** MAXP DATA *****')
    print()


def parse_name(name_data):
    print('***** NAME DATA *****')
    print()


def parse_os2(os2_data):
    print('***** OS/2 DATA *****')
    print()


def parse_post(post_data):
    print('***** POST DATA *****')
    print()


if __name__ == '__main__':
    with open('Cirka-Light.otf', 'rb') as f:
        data = f.read()

    main(data)

