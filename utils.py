def read_classification_from_file(filename):
    with open(filename, "r", encoding='utf-8') as file:
        content = file.read()
        words = content.split(); #len(words) should always be even

        file_stat = dict()

        for i in range(int(len(words)/2)):
            file_stat[words[i*2]] = words[i*2 +1]

    return file_stat

def write_classification_to_file(filename, stats):
    with open(filename, "w", encoding='utf-8') as file:
        for key in stats:
            file.write(key + ' ' + stats[key] + '\n');
    return

if __name__ == "__main__":
    test_stats = read_classification_from_file("!truth.txt")

    write_classification_to_file("test_write.txt", test_stats)
