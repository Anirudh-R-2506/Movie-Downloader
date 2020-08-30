import signal
from console_progressbar import ProgressBar
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
init()
class tr:
    def __init__(self,name):
        self.name = name
        self.temp_file = environ['userprofile']+'\\AppData\\Local\\Temp\\'+name+'.torrent'
    def versions(self):
        URL = 'https://www.google.com/search?source=hp&ei=DMZHX8SiFreJ4-EP7rW_-Ao&q='+self.name+'+site%3Atamilrockers.ws&oq='+self.name+'+site%3Atamilrockers.ws&gs_lcp=CgZwc3ktYWIQAzoOCAAQ6gIQtAIQmgEQ5QI6AggAOgIILjoICAAQsQMQgwE6BQguEJMCOggILhCxAxCDAToLCC4QsQMQgwEQkwI6BQguELEDOgUIABCxAzoICC4QsQMQkwI6BggAEBYQHlCFGVixUGDJUmgBcAB4AIABggGIAccPkgEEMjYuMZgBAKABAaoBB2d3cy13aXqwAQY&sclient=psy-ab&ved=0ahUKEwjE2OjtzrvrAhW3xDgGHe7aD68Q4dUDCAY&uact=5'
        print(colored('\n[-] GETTING AVAILABLE VERSIONS', 'green'))
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
                print(colored(menu, 'green'),end='')
                b=int(input())
            except ValueError:
                print(colored('\n[-] INVALID CHOICE', 'white', 'on_red'))
                continue
            except EOFError:
                print(colored('\n\n[-] PLEASE CHOOSE YOUR VERSION', 'white', 'on_red'))
                continue
            if b in [a+1 for a in range(len(results))]:
                url = results[b-1]['link']
                break
            else:
                print(colored('\n[-] INVALID CHOICE', 'white', 'on_red'))
        return url
    def get_torrent(self,url):
        print(colored('\n[-] CONNECTING TO PROXY SERVER', 'green'))
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent" : USER_AGENT}
        tries = 10
        while tries >= 0:
            tries -= 1
            a = FreeProxy(rand=True, timeout=0.3).get().split('://')[1]
            try:
                response = get(url,proxies={"http": a, "https": a}, headers=headers, timeout=7)
            except:
                print(colored('\n[-] ERROR CONNECTING TO PROXY '+a+'. TRYING WITH NEXT PROXY', 'white', 'on_red'))
                continue
            if response.content:
                try:
                    s = BeautifulSoup(response.content, 'html.parser')
                    torrent = s.find('a', {'title' : 'Download attachment'})['href']
                except:
                    print(colored('\n[-] ERROR CONNECTING TO PROXY '+a+'. TRYING WITH NEXT PROXY', 'white', 'on_red'))
                    continue
                print(colored('\n[-] DOWNLOADING TORRENT FILE', 'green'))
                try:
                    r = get(torrent, allow_redirects=True, proxies={"http": a, "https": a}, headers=headers)
                except:
                    continue
                open(self.temp_file, 'wb').write(r.content)
                print(colored('\n[-] DOWNLOADED TORRENT FILE', 'green'))
                return 1
            else:
                continue
        return 0
def movie_download(path):
    print(colored('\n[-] STARTING DOWNLOAD', 'green'))
    info = STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    Popen("qbittorrent.exe", startupinfo=info)
    qb = Client('http://127.0.0.1:8081/')
    qb.login('admin', 'adminadmin')
    torrent_file = open(path, 'rb')
    qb.download_from_file(torrent_file, savepath=dl_path)
    pb = ProgressBar(total=100,prefix='[-] PROGRESS', suffix='[PRESS CTRL+C TO CANCEL DOWNLOAD]', decimals=4, length=50, fill='█', zfill=' ')
    print()
    try:
        while 1:
            torrents = qb.torrents()
            b = torrents[-1]['progress']*100
            pb.print_progress_bar(b)
            if b == 100:
                qb.delete_all()
                Popen('taskkill /F /IM qbittorrent.exe /T', shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(colored('\n[-] MOVIE DOWNLOADED AT '+dl_path, 'green'))
                print(colored('\n[-] ENJOY YOUR MOVIE :)', 'green'))
                try:
                    print(colored('\n[-] PRESS ENTER TO QUIT', 'green'),end='')
                    input()
                except:
                    return
                return
    except KeyboardInterrupt:
        print(colored('\n[-] REMOVING TORRENT AND DELETING DOWNLOADED FILES', 'red'))
        qb.delete_all_permanently()
def main():
    terminal = 'mode 100,35'
    system(terminal)
    print('''
  ████████╗ █████╗ ███╗   ███╗██╗██╗     ██████╗  ██████╗  ██████╗██╗  ██╗███████╗██████╗ ███████╗
  ╚══██╔══╝██╔══██╗████╗ ████║██║██║     ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔════╝
     ██║   ███████║██╔████╔██║██║██║     ██████╔╝██║   ██║██║     █████╔╝ █████╗  ██████╔╝███████╗
     ██║   ██╔══██║██║╚██╔╝██║██║██║     ██╔══██╗██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗╚════██║
     ██║   ██║  ██║██║ ╚═╝ ██║██║███████╗██║  ██║╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║███████║
     ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝



    ''')
    while 1:
        try:
            print(colored('\n[-] ENTER MOVIE NAME(TAMIL OR TAMIL DUBBED MOVIES ONLY) ', 'green'),end='')
            i = input()
        except ValueError:
            print(colored('\n[-] INVALID MOVIE NAME', 'white', 'on_red'))
        except EOFError:
            print(colored('\n\n[-] PLEASE ENTER A MOVIE NAME ', 'white', 'on_red'))
            continue
        if ' ' in i:
            i = '%20'.join(i.split(' '))
        tamilrocker_object = tr(i)
        selected_version = tamilrocker_object.versions()
        if not selected_version:
            print(colored('\n[-] MOVIE DOES NOT EXIST IN TAMILROCKERS DATABASE. PLEASE RECHECK YOUR SPELLING IF MOVIE IS RELEASED IN THEATRES', 'white', 'on_red'))
            continue
        break
    while 1:
        try:
            print(colored('\n[-] ENTER THE FULL PATH TO DOWNLOAD THE MOVIE(PRESS ENTER FOR CURRENT FOLDER) ', 'green'),end='')
            dl_path = input()
        except ValueError:
            print(colored('\n[-] INVALID PATH', 'white', 'on_red'))
            continue
        except EOFError:
            print(colored('\n\n[-] PLEASE ENTER A PATH', 'white', 'on_red'))
            continue
        if isdir(dl_path):
            break
        elif not dl_path:
            dl_path = getcwd()
            break
        else:
            print(colored('\n[-] PATH DOES NOT EXIST', 'white', 'on_red'))
    if tamilrocker_object.get_torrent(selected_version):
        return dl_path
    else:
        return 0
if __name__ == '__main__':
    s = signal.signal(signal.SIGINT, signal.SIG_IGN)
    no_interrupt = main()
    signal.signal(signal.SIGINT, s)
    if no_interrupt:
        try:
            movie_download(no_interrupt)
        except PermissionError:
            Popen('taskkill /F /IM qbittorrent.exe /T', shell=False, stdout=PIPE, stderr=PIPE)
            print(colored('\n[-] PLEASE MOVE THE SOURCE FOLDER TO THE MAIN DRIVE OF YOUR COMPUTER AND TRY AGAIN', 'white', 'on_red'))
