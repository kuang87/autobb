import requests
import random
from datetime import datetime

config = None
msg_max_size = 4000


def notify(msg):
    global msg_max_size
    if config and 'msg_max_size' in config:
        msg_max_size = config['msg_max_size']
    file_msg = None
    if len(msg) > msg_max_size:
        file_msg = msg
        msg = msg[:msg_max_size] + "\n..."
    roomId = config['room_id']
    token = config['token']
    rnumber = random.randint(10000000, 99999999)
    if not file_msg:
        data = {
            'msgtype': 'm.text',
            'body': msg,
        }
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        return requests.put(f"https://{config['host']}/_matrix/client/r0/rooms/{roomId}/send/m.room.message/{rnumber}", json=data, headers=headers)
    else:
        # Upload file to server
        headers = {'Content-Type': 'text-plain', 'Authorization': 'Bearer ' + token}
        files = {
            'file': ('full.txt', file_msg)
        }
        response = requests.post(f"{config['host']}/_matrix/media/r0/upload", headers=headers, files=files)

        if response.status_code != 200:
            raise Exception(f"Ошибка загрузки файла: {response.text}")

        content_uri = response.json()["content_uri"]

        # Send file to room
        current_date = datetime.now().strftime("%Y-%m-%d")
        data = {
            'msgtype': 'm.file',
            'body': 'Full scan Processing ' + current_date,
            'filename': 'full.txt',
            'url': content_uri,
            'info': {
                'mimetype': 'text/plain',
                'size': len(msg)
            }
        }

        return requests.post(f"https://{config['host']}/_matrix/client/r0/rooms/{roomId}/send/m.room.message/{rnumber}", json=data, headers=headers)


if __name__=='__main__':
    import sys
    from pprint import pprint
    if len(sys.argv) != 4:
        print(f"Usage:\necho 'test' | {sys.argv[0]} API_HOST BOT_TOKEN ROOM_ID", file=sys.stderr)
        sys.exit()
    msg = sys.stdin.read()
    if len(msg.strip()) > 0:
        config = {
            'host': sys.argv[1],
            'token': sys.argv[2],
            'room_id': sys.argv[3],
        }
        pprint(vars(notify(msg)))
