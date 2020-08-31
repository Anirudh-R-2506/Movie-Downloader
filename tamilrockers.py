import signal
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from qbittorrent import Client
from os.path import isdir
from fp.fp import FreeProxy
from os import getcwd,environ,system
from subprocess import STARTUPINFO,Popen,PIPE
from colorama import init
from termcolor import colored
from sys import stdout
init()
def progress(count, total, status='',prefix=''):
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 0)
    bar = '█' * filled_len + ' ' * (bar_len - filled_len)
    last_msg_length = len(progress.last_msg) if hasattr(progress, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(colored('%s [%s] %s%s %s\r' % (prefix,bar, percents, '%', status),'white', 'on_green', attrs=['bold']),end='\r')
    progress.last_msg = '%s [%s] %s%s %s\r' % (prefix,bar, percents, '%', status)
class movie:
    class tr:
        def __init__(self,name):
            self.name = name
            self.temp_file = environ['userprofile']+'\\AppData\\Local\\Temp\\'+name+'.torrent'
        def versions(self):
            URL = 'https://www.google.com/search?source=hp&ei=DMZHX8SiFreJ4-EP7rW_-Ao&q='+self.name+'+site%3Atamilrockers.ws&oq='+self.name+'+site%3Atamilrockers.ws&gs_lcp=CgZwc3ktYWIQAzoOCAAQ6gIQtAIQmgEQ5QI6AggAOgIILjoICAAQsQMQgwE6BQguEJMCOggILhCxAxCDAToLCC4QsQMQgwEQkwI6BQguELEDOgUIABCxAzoICC4QsQMQkwI6BggAEBYQHlCFGVixUGDJUmgBcAB4AIABggGIAccPkgEEMjYuMZgBAKABAaoBB2d3cy13aXqwAQY&sclient=psy-ab&ved=0ahUKEwjE2OjtzrvrAhW3xDgGHe7aD68Q4dUDCAY&uact=5'
            print(colored('\n[-] GETTING AVAILABLE VERSIONS', 'green', attrs=['bold']))
            USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
            headers = {"user-agent" : USER_AGENT}
            resp = get(URL, headers=headers)
            soup = BeautifulSoup(resp.content, "html.parser")
            results = []
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    if 'wallpapers' in link or 'forums' in link:
                        continue
                    item = {
                        "link": link
                    }
                    results.append(item)
            if not results:
                return 0
            menu = '\n[-] SELECT VERSION\n'
            index = 0
            for a in range(len(results)):
                index += 1
                s = results[a]['link'].split('/')
                if s[-1] == '':
                    f = s[-2].split('-')
                    h = []
                    for b in range(len(f)):
                        if 'gb' in f[b]:
                            if len(f[b]) == 5:
                                c = 0
                                n = ''
                                for m in f[b]:
                                    if c == 2:
                                        n += '.'+m
                                        c += 1
                                    else:
                                        n += m
                                        c += 1
                            else:
                                c = 0
                                n = ''
                                for m in f[b]:
                                    if c == 1:
                                        n += '.'+m
                                        c += 1
                                    else:
                                        n += m
                                        c += 1
                            h.append(n)
                        else:
                            h.append(f[b])
                    if len(h) > 1:
                        menu += str(index)+') '+'-'.join(h[1:])+'\n'
                elif 'page' in s[-1]:
                    s.pop(-1)
                    results[a]['link'] = '/'.join(s)
                    f = s[-1].split('-')
                    h = []
                    for b in range(len(f)):
                        if 'gb' in f[b]:
                            c = 0
                            n = ''
                            for m in f[b]:
                                if c == 1:
                                    n += '.'+m
                                    c += 1
                                else:
                                    n += m
                                    c += 1
                            h.append(n)
                        else:
                            h.append(f[b])
                    if len(h) > 1:
                        menu += str(index)+') '+'-'.join(h[1:])+'\n'
                else:
                    f = s[-1].split('-')
                    h = []
                    for b in range(len(f)):
                        if 'gb' in f[b]:
                            if len(f[b]) == 5:
                                c = 0
                                n = ''
                                for m in f[b]:
                                    if c == 2:
                                        n += '.'+m
                                        c += 1
                                    else:
                                        n += m
                                        c += 1
                            else:
                                c = 0
                                n = ''
                                for m in f[b]:
                                    if c == 1:
                                        n += '.'+m
                                        c += 1
                                    else:
                                        n += m
                                        c += 1
                            h.append(n)
                        else:
                            h.append(f[b])
                    if len(h) > 1:
                        menu += str(index)+') '+'-'.join(h[1:])+'\n'
            while 1:
                try:
                    print(colored(menu, 'green', attrs=['bold']),end='')
                    b=int(input())
                except ValueError:
                    print(colored('\n[-] INVALID CHOICE', 'white', 'on_red', attrs=['bold']))
                    continue
                except EOFError:
                    print(colored('\n\n[-] PLEASE CHOOSE YOUR VERSION', 'white', 'on_red', attrs=['bold']))
                    continue
                if b in [a+1 for a in range(len(results))]:
                    url = results[b-1]['link']
                    break
                else:
                    print(colored('\n[-] INVALID CHOICE', 'white', 'on_red', attrs=['bold']))
            return url
        def get_torrent(self,url):
            print(colored('\n[-] CONNECTING TO PROXY SERVER', 'green', attrs=['bold']))
            l=[]
            USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
            headers = {"user-agent" : USER_AGENT}
            while 1:
                a = FreeProxy(rand=True, timeout=0.3).get().split('://')[1]
                if a in l:
                    continue
                l.append(a)
                try:
                    response = get(url,proxies={"http": a, "https": a}, headers=headers, timeout=7)
                except:
                    print(colored('\n[-] ERROR CONNECTING TO PROXY '+a+'. TRYING WITH NEXT PROXY', 'white', 'on_red', attrs=['bold']))
                    continue
                if response.content:
                    try:
                        s = BeautifulSoup(response.content, 'html.parser')
                        torrent = s.find('a', {'title' : 'Download attachment'})['href']
                    except:
                        print(colored('\n[-] ERROR CONNECTING TO PROXY '+a+'. TRYING WITH NEXT PROXY', 'white', 'on_red', attrs=['bold']))
                        continue
                    print(colored('\n[-] DOWNLOADING TORRENT FILE', 'green', attrs=['bold']))
                    try:
                        r = get(torrent, allow_redirects=True, proxies={"http": a, "https": a}, headers=headers)
                    except:
                        continue
                    open(self.temp_file, 'wb').write(r.content)
                    print(colored('\n[-] DOWNLOADED TORRENT FILE', 'green', attrs=['bold']))
                    return self.temp_file
                else:
                    continue
            return 0
def movie_download(path,torrent_path):
    print(colored('\n[-] STARTING DOWNLOAD', 'green', attrs=['bold']))
    info = STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    Popen("torrent.exe", startupinfo=info)
    qb = Client('http://127.0.0.1:8081/')
    qb.login('admin', 'adminadmin')
    torrent_file = open(torrent_path, 'rb')
    qb.download_from_file(torrent_file, savepath=path)
    try:
        while 1:
            torrents = qb.torrents()
            b = torrents[-1]['progress']*100
            progress(b,100,status='[PRESS CTRL+C TO CANCEL DOWNLOAD]',prefix='[-] DOWNLOADING')
            sleep(1)
            if b == 100:
                qb.delete_all()
                Popen('taskkill /F /IM torrent.exe /T', shell=False, stdout=PIPE, stderr=PIPE)
                print(colored('\n[-] MOVIE DOWNLOADED AT '+path, 'green', attrs=['bold']))
                print(colored('\n[-] ENJOY YOUR MOVIE :)', 'green', attrs=['bold']))
                try:
                    print(colored('\n[-] PRESS ENTER TO QUIT', 'green', attrs=['bold']),end='')
                    input()
                except:
                    return
                return
    except KeyboardInterrupt:
        print(colored('\n\n[-] REMOVING TORRENT AND DELETING DOWNLOADED FILES', 'white','on_red', attrs=['bold']))
        qb.delete_all_permanently()
        sleep(2)
        Popen('taskkill /F /IM torrent.exe /T', shell=False, stdout=PIPE, stderr=PIPE)
def main():
    terminal = 'mode 100,35'
    system(terminal)
    print(colored('''
 ████████╗ █████╗ ███╗   ███╗██╗██╗     ██████╗  ██████╗  ██████╗██╗  ██╗███████╗██████╗ ███████╗
 ╚══██╔══╝██╔══██╗████╗ ████║██║██║     ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔════╝
    ██║   ███████║██╔████╔██║██║██║     ██████╔╝██║   ██║██║     █████╔╝ █████╗  ██████╔╝███████╗
    ██║   ██╔══██║██║╚██╔╝██║██║██║     ██╔══██╗██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗╚════██║
    ██║   ██║  ██║██║ ╚═╝ ██║██║███████╗██║  ██║╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║███████║
     ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝



    ''','green', attrs=['bold']))
    while 1:
        try:
            print(colored('\n[-] ENTER MOVIE NAME(TAMIL OR TAMIL DUBBED MOVIES ONLY) ', 'green', attrs=['bold']),end='')
            i = input()
        except ValueError:
            print(colored('\n[-] INVALID MOVIE NAME', 'white', 'on_red', attrs=['bold']))
        except EOFError:
            print(colored('\n\n[-] PLEASE ENTER A MOVIE NAME ', 'white', 'on_red', attrs=['bold']))
            continue
        if ' ' in i:
            i = '%20'.join(i.split(' '))
        tamilrocker_object = movie().tr(i)
        selected_version = tamilrocker_object.versions()
        if not selected_version:
            print(colored('\n[-] MOVIE DOES NOT EXIST IN TAMILROCKERS DATABASE. PLEASE RECHECK YOUR SPELLING IF MOVIE IS RELEASED IN THEATRES', 'white', 'on_red', attrs=['bold']))
            continue
        break
    while 1:
        try:
            print(colored('\n[-] ENTER THE FULL PATH TO DOWNLOAD THE MOVIE(PRESS ENTER FOR CURRENT FOLDER) ', 'green', attrs=['bold']),end='')
            dl_path = input()
        except ValueError:
            print(colored('\n[-] INVALID PATH', 'white', 'on_red', attrs=['bold']))
            continue
        except EOFError:
            print(colored('\n\n[-] PLEASE ENTER A PATH', 'white', 'on_red', attrs=['bold']))
            continue
        if isdir(dl_path):
            break
        elif not dl_path:
            dl_path = getcwd()
            break
        else:
            print(colored('\n[-] PATH DOES NOT EXIST', 'white', 'on_red', attrs=['bold']))
    temp = tamilrocker_object.get_torrent(selected_version)
    if temp:
        return [dl_path,temp]
    else:
        return 0
if __name__ == '__main__':
    s = signal.signal(signal.SIGINT, signal.SIG_IGN)
    no_interrupt = main()
    signal.signal(signal.SIGINT, s)
    if no_interrupt:
        try:
            movie_download(torrent_path=no_interrupt[1],path=no_interrupt[0])
        except PermissionError:
            Popen('taskkill /F /IM torrent.exe /T', shell=False, stdout=PIPE, stderr=PIPE)
            print(colored('\n[-] PLEASE MOVE THE SOURCE FOLDER TO THE MAIN DRIVE OF YOUR COMPUTER AND TRY AGAIN', 'white', 'on_red', attrs=['bold']))
