config = None


def notify(msg):
    file_name = config['name']
    f = open(file_name, 'a')
    f.write(msg)
    f.close()


if __name__ == '__main__':
    import sys
    from pprint import pprint
    if len(sys.argv) != 2:
        print(f"Usage:\necho 'test' | {sys.argv[0]} reportbb.txt", file=sys.stderr)
        sys.exit()

    msg = sys.stdin.read()
    if len(msg.strip()) > 0:
        config = {
            'name': sys.argv[1],
        }
        pprint(msg)
        notify(msg)
