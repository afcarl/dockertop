#!/usr/bin/python

import os, sys
import signal
import yaml
import curses
import docker
import logging
import psutil
from time import time
from argparse import ArgumentParser

__version__='0.0.1'


class RunDockerTop(object):
    def __init__(self,config_file):
        logging.root.setLevel(logging.INFO)
        self.configdict = self.readconfig(config_file)
        self.polldocker()

    def sig_handler(self, signal, frame):
        curses.endwin()
        sys.exit(0)

    def readconfig(self, config_file):
        """
        populate a config dictionary
        """
        cnf = {}
        try:
            y=yaml.load_all(open(config_file, 'r'))
            for conf in y:
                for k,v in conf.items():
                    cnf[k] = v
        except Exception,e:
            #load defaults
            logging.info(e) 
            logging.info(('unable to load config file %s, using defaults') 
                      % (config_file))
            cnf['d_url'] = 'unix://var/run/docker.sock'
        if not cnf.has_key('d_ver'):
            cnf['d_ver'] = '1.12'
        if not cnf.has_key('timeout'):
            cnf['d_timeout'] = 10
        return cnf
    
    def polldocker(self):
        output = {}
        pids = {}
        c = docker.Client(base_url=self.configdict['d_url'],
        version=self.configdict['d_ver'], timeout=self.configdict['d_timeout'])
        s = curses.initscr()
        s.timeout(1000)
        s.border(0)
        while True:
            signal.signal(signal.SIGINT, self.sig_handler)
            s.clear()
            try:
                running = c.containers(quiet=True, all=False, trunc=True, 
                        latest=False, since=None, before=None, limit=-1)
            except Exception, e:
                logging.critical(('unable to connect to docker at %s!') % (self.configdict['d_url']))
                logging.debug(e)
                curses.endwin()
                sys.exit(0)
            #build a list of containers to pids
            for container in running:
                inspect = c.inspect_container(container['Id'])
                pids[container['Id']] = inspect['State']['Pid']
            for k in pids:
                output[k] = {}
                v = pids[k]
                try:
                    p = psutil.Process(v)
                    mem = p.get_memory_info()
                    cpu = p.get_cpu_percent()
                    exe = p.exe()
                    ctime = time() - p.create_time()
                    output[k]['name'] = c.inspect_container(cid)['Name']
                    output[k]['vm'] = "{:.2f}".format(float(mem[0]) / 1024 / 1024)
                    output[k]['rss'] = "{:.2f}".format(float(mem[1]) / 1024 / 1024)
                    output[k]['cpu'] = cpu
                    output[k]['rtime'] = str("{:.3f}".format(ctime / 60))
                    output[k]['exe'] = exe
                except:
                    del pids[k]
                    pass
            s.addstr(2, 2, "NAME")
            s.addstr(2, 18, "CID")
            s.addstr(2, 34, "CPU")
            s.addstr(2, 41, "VM")
            s.addstr(2, 48, "RSS")
            s.addstr(2, 54, "EXE")
            s.addstr(2, 71, "UPTIME")
            cid_line = 4
            for cid in output:
                s.addstr(cid_line, 2, output[cid]['name'])
                s.addstr(cid_line, 18, cid[:12])
                s.addstr(cid_line, 34, str(output[cid]['cpu']))
                s.addstr(cid_line, 41, output[cid]['vm'])
                s.addstr(cid_line, 48, output[cid]['rss'])
                s.addstr(cid_line, 54, output[cid]['exe'])
                s.addstr(cid_line, 71, output[cid]['rtime'])
                cid_line += 1
            s.refresh()
            x = s.getch()
            if x == ord('q'):
                break
        curses.endwin()
            

def main():
    parser = ArgumentParser(description='Dockertop %s' % __version__)
    parser.add_argument('-c', dest='config_path', help='Path to your config file', default='~/.dockertoprc')
    args = parser.parse_args()
    config_path = os.path.expanduser(args.config_path)
    #run
    dt = RunDockerTop(config_file=args.config_path)

if __name__ == '__main__':
    main()
