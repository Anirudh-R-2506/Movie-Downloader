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
from tqdm import tqdm
init()
class movie:
    class tr:
        def __init__(self,name,lang):
            self.name = name
            self.temp_file = environ['userprofile']+'\\AppData\\Local\\Temp\\'+name+lang+'.torrent'
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
                    li = [a for a in self.name.lower().split('%20')]
                    vari = 1 if [a for a in li if a in link]==li else 0
                    if 'wallpapers' in link or 'forums' in link and not vari:
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
                        menu += str(index)+') '+' '.join(h[1:])+'\n'
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
                        menu += str(index)+') '+' '.join(h[1:])+'\n'
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
                        menu += str(index)+') '+' '.join(h[1:])+'\n'
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
    class eng:
        def __init__(self,name,lang):
            self.name = name
            self.temp_file = environ['userprofile']+'\\AppData\\Local\\Temp\\'+name+lang+'.torrent'
        def versions(self):
            URL = 'https://www.google.com/search?source=hp&ei=DMZHX8SiFreJ4-EP7rW_-Ao&q='+self.name+'+site%3Ayifytorrenthd.net&oq='+self.name+'+site%3Ayifytorrenthd.net&gs_lcp=CgZwc3ktYWIQAzoOCAAQ6gIQtAIQmgEQ5QI6AggAOgIILjoICAAQsQMQgwE6BQguEJMCOggILhCxAxCDAToLCC4QsQMQgwEQkwI6BQguELEDOgUIABCxAzoICC4QsQMQkwI6BggAEBYQHlCFGVixUGDJUmgBcAB4AIABggGIAccPkgEEMjYuMZgBAKABAaoBB2d3cy13aXqwAQY&sclient=psy-ab&ved=0ahUKEwjE2OjtzrvrAhW3xDgGHe7aD68Q4dUDCAY&uact=5'
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
                    li = [a for a in self.name.lower().split('%20')]
                    vari = 1 if [a for a in li if a in link]==li else 0
                    if not vari or 'page' in link.split('?')[-1]:
                        continue
                    item = {
                        "link": link
                    }
                    results.append(item)
            URL = 'https://yts.mx/browse-movies/'+self.name+'/all/all/0/latest/0/all'
            USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
            headers = {"user-agent" : USER_AGENT}
            resp = get(URL, headers=headers)
            soup = BeautifulSoup(resp.content, "html.parser")
            for g in soup.find_all('a', class_='browse-movie-link'):
                link = g['href']
                li = [a for a in self.name.lower().split('%20')]
                vari = 1 if [a for a in li if a in link]==li else 0
                if not vari or 'page' in link.split('?')[-1]:
                    continue
                item = {
                    "link": link
                }
                results.append(item)
            if not results:
                return 0
            menu = '\n[-] SELECT MOVIE\n'
            index = 0
            for a in range(len(results)):
                index += 1
                s = results[a]['link'].split('/')
                if ' '.join(s[-1].split('-')) in menu or ' '.join(s[-1].split('-')[1:]) in menu:
                    results.pop(a)#bug
                    continue
                if s[2] == 'yifytorrenthd.net':
                    menu += str(index)+') '+' '.join(s[-1].split('-')[1:])+'\n'
                else:
                    menu += str(index)+') '+' '.join(s[-1].split('-'))+'\n'
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
                try:
                    response = get(url, headers=headers, timeout=7)
                except:
                    print(colored('\n[-] ERROR WHILE RETIRIEVING TORRENT. TRYING AGAIN', 'white', 'on_red', attrs=['bold']))
                    continue
                if response.content:
                    if 'yifytorrenthd' in url:
                        res = []
                        try:
                            s = BeautifulSoup(response.content, 'html.parser')
                            torrents = s.find_all('div',class_='torrent-type')[0]
                            anchor = torrents.find_all('a')
                            for a in anchor:
                                dict = {
                                    'link':a['href'],
                                    'title':a.contents[-1]
                                }
                                res.append(dict)
                        except:
                            print(colored('\n[-] ERROR CONNECTING TO PROXY '+a+'. TRYING WITH NEXT PROXY', 'white', 'on_red', attrs=['bold']))
                            continue
                    else:
                        res = []
                        try:
                            s = BeautifulSoup(response.content, 'html.parser')
                            torrents = s.find_all('p',class_='hidden-md hidden-lg')[0]
                            anchor = torrents.find_all('a')
                            for a in anchor:
                                dict = {
                                    'link':a['href'],
                                    'title':a.contents[1]
                                }
                                res.append(dict)
                            res.pop(-1)
                        except:
                            print(colored('\n[-] ERROR CONNECTING TO PROXY '+a+'. TRYING WITH NEXT PROXY', 'white', 'on_red', attrs=['bold']))
                            continue
                    torrent = ''
                    while 1:
                        try:
                            inp_m = '\n[-] SELECT QUALITY OF MOVIE\n'
                            for a in range(1,len(res)+1):
                                inp_m += str(a)+')'+res[a-1]['title']+'\n'
                            print(colored(inp_m,'green',attrs=['bold']),end='')
                            nm = int(input())
                            if nm in [a for a in range(1,len(res)+1)]:
                                torrent = res[nm-1]['link']
                                break
                            else:
                                print(colored('\n[-] INVALID CHOICE', 'white', 'on_red', attrs=['bold']))
                        except EOFError:
                            print(colored('\n[-] PLEASE CHOOSE YOUR VERSION', 'white', 'on_red', attrs=['bold']))
                        except ValueError:
                            print(colored('\n[-] INVALID CHOICE', 'white', 'on_red', attrs=['bold']))
                    print(colored('\n[-] DOWNLOADING TORRENT FILE', 'green', attrs=['bold']))
                    try:
                        r = get(str(torrent), allow_redirects=True, headers=headers)
                    except Exception as e:
                        print(e)
                        return 0
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
    bar = tqdm(total=100, desc='[-] DOWNLOADING(PRESS CTRL+C TO CANCEL)')
    qb.download_from_file(torrent_file, savepath=path)
    try:
        while 1:
            torrents = qb.torrents()
            b = torrents[-1]['progress']
            if b >= 1:
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
            else:
                bar.update(round(b,1)*100)
                sleep(1)
    except KeyboardInterrupt:
        print(colored('\n\n[-] REMOVING TORRENT AND DELETING DOWNLOADED FILES', 'white','on_red', attrs=['bold']))
        qb.delete_all_permanently()
        sleep(2)
        Popen('taskkill /F /IM torrent.exe /T', shell=False, stdout=PIPE, stderr=PIPE)
    except:
        pass
def main():
    terminal = 'mode 100,35'
    system(terminal)
    print(colored('''
███╗   ███╗ ██████╗ ██╗   ██╗██╗███████╗    ██████╗ ██╗██████╗  █████╗ ████████╗███████╗
████╗ ████║██╔═══██╗██║   ██║██║██╔════╝    ██╔══██╗██║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
██╔████╔██║██║   ██║██║   ██║██║█████╗      ██████╔╝██║██████╔╝███████║   ██║   █████╗
██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██║██╔══╝      ██╔═══╝ ██║██╔══██╗██╔══██║   ██║   ██╔══╝
██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ██║███████╗    ██║     ██║██║  ██║██║  ██║   ██║   ███████╗
╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝



''','green', attrs=['bold']))
    while 1:
        try:
            print(colored('\n[-] ENTER MOVIE NAME ', 'green', attrs=['bold']),end='')
            i = input()
        except ValueError:
            print(colored('\n[-] INVALID MOVIE NAME', 'white', 'on_red', attrs=['bold']))
        except EOFError:
            print(colored('\n\n[-] PLEASE ENTER A MOVIE NAME ', 'white', 'on_red', attrs=['bold']))
            continue
        if ' ' in i:
            i = '%20'.join(i.split(' '))
        while 1:
            try:
                lan_l = ['tamil','english']
                inp_m = '\n[-] SELECT MOVIE LANGUAGE\n'
                in_a = 0
                for a in lan_l:
                    in_a += 1
                    inp_m += str(in_a)+') '+a.upper()+'\n'
                print(colored(inp_m,'green',attrs=['bold']),end='')
                nm = int(input())
                if nm in [a for a in range(1,len(lan_l)+1)]:
                    lan = lan_l[nm-1]
                    break
                else:
                    print(colored('\n[-] INVALID CHOICE', 'white', 'on_red', attrs=['bold']))
            except EOFError:
                print(colored('\n[-] PLEASE CHOOSE YOUR VERSION', 'white', 'on_red', attrs=['bold']))
            except ValueError:
                print(colored('\n[-] INVALID CHOICE', 'white', 'on_red', attrs=['bold']))
        movie_object = movie()
        if lan == 'tamil':
            movies = movie_object.tr(i,lan)
            selected_version = movies.versions()
            if not selected_version:
                print(colored('\n[-] MOVIE IN THAT LANGUAGE DOES NOT EXIST IN OUR DATABASE. PLEASE RECHECK YOUR SPELLING IF MOVIE IS RELEASED IN THEATRES', 'white', 'on_red', attrs=['bold']))
                continue
        elif lan == 'english':
            movies = movie_object.eng(i,lan)
            selected_version = movies.versions()
            if not selected_version:
                print(colored('\n[-] MOVIE IN THAT LANGUAGE DOES NOT EXIST IN OUR DATABASE. PLEASE RECHECK YOUR SPELLING IF MOVIE IS RELEASED IN THEATRES', 'white', 'on_red', attrs=['bold']))
                continue
        break
    while 1:
        try:
            print(colored('\n[-] ENTER THE FULL PATH TO DOWNLOAD THE MOVIE(PRESS ENTER FOR CURRENT FOLDER) ', 'green', attrs=['bold']),end='')
            dl_path = input()
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
    temp = movies.get_torrent(selected_version)
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
