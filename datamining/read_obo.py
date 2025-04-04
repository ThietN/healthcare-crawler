import os


def read_obo_debug(path=None):
    if path is None:
        path = './symp.obo'  # File mặc định

    if not os.path.exists(path):
        print(f"⚠️ File '{path}' không tồn tại!")
        return

    with open(path, encoding='utf-8') as fp:
        term_count = 0
        for line in fp:
            if '[Term]' in line:
                term_count += 1
                print(f'\n🔹 Term {term_count} bắt đầu:')
            elif ':' in line:
                key, value = line.split(':', 1)
                print(f'➡ {key.strip()}: {value.strip()}')


# Gọi hàm mà không cần truyền path
read_obo_debug()
