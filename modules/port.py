import logging
from subprocess import Popen, PIPE
from config import config
import json
from _thread import start_new_thread


def process_errors(stderr):
    with stderr:
        for line in stderr:
            print(line, end="")


def portprobes(domains, scan_ports):
    """naabu on domains search fo ports"""
    naabu_cmd = config["naabu"]['cmd'].copy()
    naabu_cmd.extend(['-p', scan_ports ])
    logging.info(' '.join(naabu_cmd))

    proc = Popen(naabu_cmd, text=True, bufsize=1, stderr=PIPE, stdout=PIPE, stdin=PIPE, errors="backslashreplace")

    start_new_thread(process_errors, (proc.stderr,))
    start_new_thread(stdinwrite, (domains, proc.stdin))


    # add scope from origin domains
    for line in proc.stdout:
        print(line, end="")
        port = json.loads(line.strip())
        #ip portscan fix
        if 'host' not in port:
            port['host'] = port['ip']

        port_scope = next( (x['scope'] for x in domains if x['host'] == port['host']), None )
        if port_scope:
            port['scope'] = port_scope
        
        yield port



def stdinwrite(domains, stdin):
    incount = 0
    with stdin:
        for d in domains:
            stdin.write(d["host"] + "\n")
            incount += 1
    logging.info(f"{incount} items writed to stdin")
