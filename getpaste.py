print('''
   ██████  ███████ ████████ ██████   █████  ███████ ████████ ███████ 
  ██       ██         ██    ██   ██ ██   ██ ██         ██    ██      
  ██   ███ █████      ██    ██████  ███████ ███████    ██    █████   
  ██    ██ ██         ██    ██      ██   ██      ██    ██    ██      
   ██████  ███████    ██    ██      ██   ██ ███████    ██    ███████ 
                                                                   
Многопоточный загрузчик паст из пабликов ВКонтакте (а может и не паст)  

Токен от страницы можно получить здесь: https://vkhost.github.io/''')

from threading import Thread
import vk_api
import os
import random
#vk_api.VkApi.RPS_DELAY = 1/6

tokenwrite = True
while tokenwrite:
    token = input(" >>> Введите токен от страницы ВКонтакте: ")
    if len(token) != 85:
        print('[!] Введён токен, длина которого не равна 85 символам. Попробуйте снова. Убедитесь, что нету пробела в конце или чего либо подобного')
    else:
        print("[*] Проверка токена...")
        try:
            vk = vk_api.VkApi(token=token).get_api()
            vk.users.get(user_id=1)
            print("[V] Доступ к VK_API получен!")
            tokenwrite = False
        except Exception as e:
            print(f'[X] Токен не подходит: \n{"-" * len(str(e))}\n{str(e)}\n{"-" * len(str(e))}\nПопробуйте снова.')

print("""
Теперь нам необходимо получить список пабликов.
Вводите короткие имена (к примеру, internetpasta или club123123123)
Чтобы окончить ввод имён, введите end""")

adding = True
addreses = []
while adding:
    if adding:
        ch = input(f"Имён: {str(len(addreses))} ~ > ")
        if ch == "end":
            adding = False
            if len(addreses) == 0:
                print("[X] Указано 0 адресов, выполняется выход из программы. ")
                exit(0)
        else:
            addreses.append(ch)

print(" >>> Адреса получены. Получается, список таков: ")
for x in addreses:
    print("https://vk.com/" + x)

setdir = True
while setdir:
    dirname = input(' >>> Введите название папки для сохранения паст: ')
    if dirname in os.listdir('.'):
        if os.path.isdir(dirname):
            filescount = os.listdir(dirname)
            c = input(f'Папка {dirname} существует и содержит {str(len(filescount))} файлов. Вы действительно хотите указать эту папку? [Y/N]: ')
            if c.lower() == 'y':
                print('Фокус поставлен на папку ' + dirname + '.')
                setdir = False
            elif c.lower() == 'n':
                pass
            else:
                print(f'Сигнал "{c}" не распознан.')
    else:
        if dirname not in os.listdir('.'):
            os.mkdir(dirname)
            print(f'Папка {dirname} создана.')
        print('Фокус поставлен на папку ' + dirname + '.')
        setdir = False

def getrandomid():
    charset = '1234567890qazxswedcvfrtgbnhyujmkiolp'
    result = ''
    for x in range(10):
        result += random.choice(list(charset))
    return result

def writeto(text, target):
    file = open(str(target), 'w', encoding='utf-8')
    file.write(str(text))
    file.close()

def fetcher(myid, startfrom, id):
    ftch = True
    while ftch:
        try:
            fetch = vk.wall.getById(posts=f"{id}_{str(startfrom)}")[0]['text']
            #print(f'Debug: \n{"-" * len(str(fetch2))}\n{str(fetch2)}\n{"-" * len(str(fetch2))}\n')
            if len(fetch) < 100:
                print(f"[Fetcher-{str(myid)}] Не похоже на пасту, меньше 100 символов. Не сохраняю")
            else:
                fid = getrandomid()
                writeto(fetch, f'{dirname}/{fid}.txt')
                print(f"[Fetcher-{str(myid)}] Паста [{fetch[:50]}...] сохранена в файл {dirname}/{fid}.txt")
        except Exception as e:
            #print(f"[Fetcher-{str(myid)}] Не удалось скачать пост {id}_{startfrom}. Удалённая запись? | Вызвано: {str(e)}")
            pass
        startfrom = int(startfrom) - 1
        if str(startfrom).startswith("-"):
            print(f"[Fetcher-{str(myid)}] Завершаю свою работу...")

print('[*] Подготовка...')
ids = []
for x in addreses:
    try:
        ids.append('-' + str(vk.groups.getById(group_id=x)[0]["id"]))
    except Exception as e:
        print(f"[!] Паблик https://vk.com/{x} не найден. Он будет убран из списка. | Вызвано: {str(e)}")

for x in ids:
    try:
        cnt = vk.wall.get(owner_id=x, count=1)['items'][0]['id']
        #print(f'Debug: \n{"-" * len(str(cnt))}\n{str(cnt)}\n{"-" * len(str(cnt))}\n')
        exec(f"fetcher_{ids.index(x)} = Thread(target=fetcher, args=({ids.index(x)}, cnt, x,))")
        exec(f"fetcher_{ids.index(x)}.start()")
        print(f'[Основной поток] Fetcher-{ids.index(x)} успешно запущен!')
    except Exception as e:
        print(f'[Основной поток] Не удалось запустить Fetcher-{ids.index(x)} :( | Вызвано: {str(e)}')