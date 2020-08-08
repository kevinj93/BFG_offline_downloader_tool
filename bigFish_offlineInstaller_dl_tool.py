# BigFish Offline Installer Download Tool V1.0

import datetime
import os
import time
import wget
import sys
import shutil
import urllib.request
from pathlib import Path

title = 'BigFish Offline Installer Download Tool V1.0'
os.system('color 02')

if 'bfginstallercreator.file' not in os.listdir():
    print(title + '\n\n')
    print('Error: bfginstallercreator.file is missing. Make sure to place the file in the same folder as the script and try again!')
    os.system('pause >nul')
    sys.exit()
elif 'bfginstallercreator.file' in os.listdir() and Path('bfginstallercreator.file').stat().st_size != 237568:
    print(title + '\n\n')
    print('Error: bfginstallercreator.file size mismatch! Make sure the good file is there and try again!')
    os.system('pause >nul')
    sys.exit()
elif 'bfginstallercreator.file' in os.listdir() and Path('bfginstallercreator.file').stat().st_size == 237568:
    if not os.path.isdir('BigFish Offline Downloader'):
        os.mkdir('BigFish Offline Downloader')
    shutil.copy('bfginstallercreator.file', './BigFish Offline Downloader/bfginstallercreator.file')

for file in os.listdir():
    if '.exe' in file and 'gF' in file:
        shutil.move(file, './BigFish Offline Downloader/' + file)

os.chdir('./BigFish Offline Downloader')
if not os.path.isdir('DOWNLOADED'):
    os.mkdir('DOWNLOADED')

for file_ in os.listdir():
    if '.reg' in file_:
        os.remove(file_)

if not os.path.isdir('FAILED_RETRIES'):
    os.mkdir('FAILED_RETRIES')

txtfile_in_dir = False

if 'wrapidlist.txt' in os.listdir() or 'wrapidlist.txt' in os.listdir('../'):
    txtfile_in_dir = True

regdir_x86 = '\"HKLM\\SOFTWARE\\Big Fish Games\\Persistence\\GameDB\\'
regdir_x64 = '\"HKLM\\SOFTWARE\\WOW6432Node\\Big Fish Games\\Persistence\\GameDB\\'

regdir_installed_x86 = '\"HKLM\\SOFTWARE\\Big Fish Games\\Persistence\\Install\\'
regdir_installed_x64 = '\"HKLM\\SOFTWARE\\WOW6432Node\\Big Fish Games\\Persistence\\Install\\'

print(title + '\n')
is_x64 = False
if os.path.isdir('C:\\Program Files (x86)\\'):
    is_x64 = True
    print('64-bit System detected. \n')
    mainregdir = regdir_x64
else:
    print('32-bit System detected. \n')
    mainregdir = regdir_x86

invalid_chars = '<>:"/\\|?*'
games_DL = dict()
games_not_DL = dict()
no_tries_by_wrapid = dict()
total_downloaded = 0

start = datetime.datetime.now()
app_start = '%d/%d/%d %.2d:%.2d:%.2d' % (start.day, start.month, start.year, start.hour, start.minute, start.second)

wrapIDs_before_install = []
already_downloaded = []
failed_wrapid = []
regfailed_attempts = 0
timerval = 0.0


def create_installer_bywrapid(txtfile):
    txtf = open(txtfile, 'r')
    txtfrd = txtf.readlines()
    installers_to_make = []
    bf_installername_prefix = 'abcdefg_g'
    bf_installername_suffix = '_d123456789.exe'
    for line in txtfrd:
        if 'F' in line:
            if 'L1' in line or 'L2' in line or 'L3' in line or 'L4' in line or 'L7' in line or 'L8' in line or 'L10' in line or 'L11' in line or 'L12' in line or 'L13' in line:
                cleanstring = line.rstrip()
                current_installername = bf_installername_prefix + cleanstring.lstrip() + bf_installername_suffix
                installers_to_make.append(current_installername)
    for installer in installers_to_make:
        shutil.copyfile('bfginstallercreator.file', installer)


def recreate_installer_regnodl(wrapid):
    if no_tries_by_wrapid[wrapid] < 3:
        bf_installername_prefix = 'abcdefg_g'
        bf_installername_suffix = '_d123456789.exe'
        installer_name = bf_installername_prefix + wrapid + bf_installername_suffix
        shutil.copyfile('bfginstallercreator.file', installer_name)


#  Duplicate Cleanup Before Download
def cleanup():
    for _file in os.listdir():
        if '.exe' in _file and 'gF' in _file:
            _filedata = _file.split('_')
            for _data in _filedata:
                if _data.startswith('gF'):
                    _current_wrapID = _data[1:]
                    wrapIDs_before_install.append(_current_wrapID)
    for wrapid in wrapIDs_before_install:
        for folder in os.listdir('./DOWNLOADED/'):
            if os.path.isdir('./DOWNLOADED/' + folder) and wrapid in folder and folder != wrapid:
                already_downloaded.append(wrapid)
    for game in already_downloaded:
        for _file in os.listdir():
            if '.exe' in _file and 'gF' in _file and game in _file:
                os.remove(_file)
    for failed_game_folder in os.listdir():
        for element in wrapIDs_before_install:
            if element == failed_game_folder:
                shutil.rmtree(failed_game_folder)
    if 'Failed' in os.listdir():
        shutil.rmtree('Failed')


def validated_input(user__input):
    isValidInput = False
    try:
        user_input = float(user__input)
        if 0.1 <= user_input <= 20:
            isValidInput = True
            return isValidInput
        else:
            return isValidInput
    except:
        if user__input == 'x':
            isValidInput = True
            return isValidInput
        else:
            return isValidInput


def reg_cleanup_pre_download():
    # REGISTRY ENTRY CLEANUP
    for wrapid in wrapIDs_before_install:
        if is_x64:
            os.system('reg delete ' + regdir_x64 + wrapid + '\" /f >nul 2> nul')
            os.system('reg delete ' + regdir_installed_x64 + wrapid + '\" /f >nul 2> nul')
        else:
            os.system('reg delete ' + regdir_x86 + wrapid)
            os.system('reg delete ' + regdir_installed_x86 + wrapid + '\" /f >nul 2> nul')


def load_dl_tasks_to_var():
    for file__ in os.listdir():  # load download tasks to a variable
        if '.exe' in file__ and 'gF' in file__:
            filedata = file__.split('_')
            for data in filedata:
                if data.startswith('gF'):
                    current_wrapID = data[1:]
                    no_tries_by_wrapid[current_wrapID] = 0


def calculate_size(total_size_bytes):
    if total_size_bytes < 1024:
        return str(total_size_bytes) + ' Bytes'
    elif 1024 <= total_size_bytes < 1048576:
        return '%.2f' % (total_size_bytes/1024) + ' KB'
    elif 1048576 <= total_size_bytes < 1073741824:
        return '%.2f' % (total_size_bytes/1048576) + ' MB'
    elif 1073741824 <= total_size_bytes < 1099511627776:
        return ('%.2f' % (total_size_bytes/1073741824)) + ' GB'
    elif 1099511627776 <= total_size_bytes < 1099511627776:
        return ('%.2f' % (total_size_bytes/1099511627776)) + ' TB'


def start_program(timer):
    os.system('taskkill /F /IM bfgclient.exe >nul 2> nul')  # Kill bfgclient if running.

    for file in os.listdir():

        if '.exe' in file and 'gF' in file:
            current_installername = file
            print('Current installer: ' + file)
            filedata = file.split('_')
            for data in filedata:
                if data.startswith('gF'):
                    current_wrapID = data[1:]

                    print('Detected wrapID: ' + current_wrapID)
                    # os.system('reg delete \"HKLM\\SOFTWARE\\Big Fish Games\\Persistence\\Install\\' + current_wrapID + '\" /f >nul 2> nul')
            if len(current_wrapID) > 1:
                print('Starting download in BigFish Game Manager ...')
                os.system(file)
                time.sleep(timer)
                print('Closing BigFish Game Manager, please wait ...')
                os.system('taskkill /F /IM bfgclient.exe >nul 2> >nul')
                print('Exporting registry file with wrapID ' + current_wrapID + ' to current directory, please wait ...')

                if current_wrapID + '.reg' not in os.listdir():
                    os.system('reg export ' + mainregdir + current_wrapID + "\" " + current_wrapID + '.reg >nul 2> nul')

                print('Reading registry file...')

                try:
                    wrapfile = open(current_wrapID + '.reg', 'r', encoding='utf-16')
                    freader = wrapfile.readlines()
                    print('Creating folder with wrapID ' + current_wrapID)
                    if not os.path.isdir(current_wrapID):
                        os.mkdir(current_wrapID)
                    else:
                        os.rmdir(current_wrapID)
                        os.mkdir(current_wrapID)

                    links_s1 = []
                    links_s2 = []
                    links_s3 = []
                    good_exe_size = 0
                    all_exe_urls = []
                    good_exe_found = False
                    exe_sizes = []  # in case of filesegmentsize mismatch
                    complete_links = []
                    dl_size = 0
                    for line in freader:
                        if '"Name"' in line:
                            currentGameName = line.split("\"=\"")[1][:-2]
                            print('Current Game: ' + line.split("\"=\"")[1][:-2])
                        elif '"urlName"' in line and '.exe' not in line:
                            links_s1.append(line.split("\"=\"")[1][:-2])
                        elif '"urlName2"' in line and '.exe' not in line:
                            links_s2.append(line.split("\"=\"")[1][:-2])
                        elif '"urlName3"' in line and '.exe' not in line:
                            links_s3.append(line.split("\"=\"")[1][:-2])
                        elif '"fileSegmentSize"' in line:  # TEST THIS
                            dl_size += int(line.split("\"=\"")[1][:-2])

                    isFound_filesegmentsize = False

                    for index, line in enumerate(freader):
                        if 'urlName3' in line and '.exe' in line:
                            fileSegmentSize_idx = index
                            isFound_filesegmentsize = True

                    if isFound_filesegmentsize:
                        for index, line in enumerate(freader):
                            if index == fileSegmentSize_idx + 1:
                                good_exe_size = line.split('"="')[1][:-2]

                        for line in freader:
                            if 'urlName' in line and '.exe' in line:
                                all_exe_urls.append(line.split('"="')[1][:-2])

                        if len(links_s1) == len(links_s2) == len(links_s3):
                            link_len = len(links_s1)

                        for i in range(link_len):
                            complete_links.append([links_s1[i], links_s2[i], links_s3[i]])

                        print('Opening gameFolder with wrapID ' + current_wrapID)
                        os.chdir('./' + current_wrapID)
                        print('Total Links found:' + str(len(complete_links) + 2))
                        print('Download Size: ' + calculate_size(dl_size))

                        exe_dl_failed = 0

                        for link in all_exe_urls:
                            if 'binswest' not in link:
                                for i in range(10):
                                    try:
                                        print('Downloading ' + link + ' ...')
                                        wget.download(link)
                                        print(' Success!')
                                        exe_dl_failed = 0
                                        download_failed = False
                                    except:
                                        print('Download failed, retrying ...')
                                        exe_dl_failed += 1
                                    else:
                                        break
                        if len(complete_links) >= 1:
                            for link in complete_links:
                                failed_attempts = 0
                                download_failed = False

                                for server_link in link:
                                    downloaded = False
                                    for i in range(5):
                                        try:
                                            print('Downloading ' + server_link)
                                            wget.download(server_link)
                                            print(' Success!')
                                            downloaded = True

                                        except:
                                            #  print(server_link + ' failed.') #  Debug
                                            failed_attempts += 1
                                            print('failed attempts: ' + str(failed_attempts))
                                            print('Download failed, retrying...')
                                        else:
                                            break
                                    if downloaded:
                                        break
                                if failed_attempts == 15:
                                    download_failed = True
                                    break

                        if not download_failed and exe_dl_failed < 2:

                            print('Renaming current game files, please wait...')
                            for gamefile in os.listdir():
                                if '.zip' in gamefile:
                                    fn = gamefile.split('.zip')
                                    os.rename(gamefile, current_wrapID + '.zip' + fn[1])
                            for gamefile in os.listdir():  # if exe size matches with registry entry
                                if '.exe' in gamefile and Path(gamefile).stat().st_size == int(good_exe_size):
                                    good_exe_found = True
                                    os.rename(gamefile, current_wrapID + '.exe')
                                    os.mkdir('goodexe')  # make a temporary folder and move the good exe there
                                    shutil.move('./' + current_wrapID + '.exe', './goodexe/' + current_wrapID + '.exe')
                                    break
                            for gamefile in os.listdir():  # remove bad/duplicate exes
                                if '.exe' in gamefile and good_exe_found:
                                    os.remove(gamefile)
                                    shutil.move('./goodexe/' + current_wrapID + '.exe', './' + current_wrapID + '.exe')  # move good exe back to installer dir after cleanup
                                elif '.exe' in gamefile and not good_exe_found:
                                    exe_sizes.append(Path(gamefile).stat().st_size)
                                    if len(exe_sizes) > 1 and exe_sizes[0] == exe_sizes[1]:  # remove second duplicate exe
                                        os.rename(gamefile, current_wrapID + '.exe')
                                        for file in os.listdir():
                                            if ' ' in file:
                                                os.remove(file)
                                        break

                            if os.path.isdir('goodexe'):
                                os.rmdir('goodexe')

                            print('Game with wrapID ' + current_wrapID + ' finished successfully.')
                            no_tries_by_wrapid.pop(current_wrapID)
                            global total_downloaded
                            total_downloaded += dl_size
                            wrapfile.close()
                            valid_filename = ''
                            for char in currentGameName:
                                if char not in invalid_chars:
                                    valid_filename += char
                                elif char in invalid_chars:
                                    valid_filename += ' - '
                            os.chdir('../')
                            if not os.path.isdir(current_wrapID + ' - ' + valid_filename):
                                os.rename(current_wrapID, current_wrapID + ' - ' + valid_filename)
                            print('Cleaning up ...')
                            if is_x64:
                                os.system('reg delete ' + regdir_x64 + current_wrapID + '\" /f >nul 2> nul')
                                os.system('reg delete ' + regdir_installed_x64 + current_wrapID + '\" /f >nul 2> nul')
                            else:
                                os.system('reg delete ' + regdir_x86 + current_wrapID + '\" /f >nul 2> nul')
                                os.system('reg delete ' + regdir_installed_x86 + current_wrapID + '\" /f >nul 2> nul')
                            if current_installername in os.listdir():
                                os.remove(current_installername)
                            if current_wrapID + '.reg' in os.listdir():
                                os.remove(current_wrapID + '.reg')
                            games_DL[current_wrapID] = [currentGameName]
                            games_DL[current_wrapID].append(dl_size)
                        else:
                            print('All Download Attempts for current game failed, Server not responding or (one of) the file(s) do not exist.')
                            games_not_DL[current_wrapID] = currentGameName
                            shutil.move('../' + file, '../FAILED_RETRIES/' + file)

                            print('Cleaning up ...')
                            wrapfile.close()
                            no_tries_by_wrapid.pop(current_wrapID)
                            if is_x64:
                                os.system('reg delete ' + regdir_x64 + current_wrapID + '\" /f >nul 2> nul')
                                os.system('reg delete ' + regdir_installed_x64 + current_wrapID + '\" /f >nul 2> nul')
                            else:
                                os.system('reg delete ' + regdir_x86 + current_wrapID + '\" /f >nul 2> nul')
                                os.system('reg delete ' + regdir_installed_x86 + current_wrapID + '\" /f >nul 2> nul')
                            os.chdir('../')
                            os.system('del ' + current_wrapID + '.reg /q')
                            shutil.rmtree(current_wrapID)
                            failed_wrapid.append(current_wrapID)
                    else:
                        print('''URLs Not found in Registry, Possibly the game has finished downloading before fetching registry file or the game was already installed.
                        
                        1- Game finished downloading before fetching registry file with links
                        2- Game is already installed
                        3- Game files do not exist anymore.        ''')

                        if file in os.listdir() and no_tries_by_wrapid[current_wrapID] == 3:
                            shutil.move(file, './FAILED_RETRIES/' + file)

                        if file in os.listdir():  # Might not be necessary
                            os.remove(file)

                        failed_wrapid.append(current_wrapID)
                        games_not_DL[current_wrapID] = file
                        recreate_installer_regnodl(current_wrapID)

                        if no_tries_by_wrapid[current_wrapID] == 3:  # after maximum tries
                            no_tries_by_wrapid.pop(current_wrapID)
                        else:
                            no_tries_by_wrapid[current_wrapID] += 1

                except:
                    print('Error, Registry file does not exist! Timer too low?!')
                    no_tries_by_wrapid.pop(current_wrapID)
                    shutil.move(current_installername, './FAILED_RETRIES/' + current_installername)
                    global regfailed_attempts
                    regfailed_attempts += 1


bfg_not_installed_msg = 'BigFish Client is not installed. Exiting...'

# 64-bit check
if is_x64:
    if not os.path.isdir('C:\\Program Files (x86)\\bfgclient'):
        print(bfg_not_installed_msg)
        sys.exit()
# 32-bit check
else:
    if not os.path.isdir('C:\\Program Files\\bfgclient'):
        print(bfg_not_installed_msg)
        sys.exit()

if txtfile_in_dir:
    print(
        'Text file with wrapIDs detected. Would you like to use it to download games by WrapID?, Type "y" for yes and "n" for no.')
    user_answered = False
    while not user_answered:
        user_answer = input('')
        if user_answer == 'y':
            if 'wrapidlist.txt' in os.listdir():
                create_installer_bywrapid('wrapidlist.txt')
            elif 'wrapidlist.txt' in os.listdir('../'):
                create_installer_bywrapid('../wrapidlist.txt')
            user_answered = True
        elif user_answer == 'n':
            user_answered = True
        else:
            print('Invalid choice, please type your choice and press Enter.')
# Pre Download Optimization

cleanup()
reg_cleanup_pre_download()
load_dl_tasks_to_var()  # Load Download Tasks to a variable

no_bf_installers_in_dir = 0

for _file_ in os.listdir():
    if '.exe' in _file_ and 'gF' in _file_:
        no_bf_installers_in_dir += 1

if no_bf_installers_in_dir <= 0:
    print(
        'No Bigfish Installers found. Make sure to put the installers in the same folder as the script and restart the program again.\nNote: Game installers for already downloaded games are automatically removed. \n')
    print('''Note #2: To Download Games by their WrapID, create a file called wrapidlist.txt, place each wrapID in a separate line, then restart the script.
    Example wrapidlist.txt:
    F123456L1
    F345678L1
    F654321L1
    ''')
    os.system('pause >nul')
    sys.exit()
else:
    print('''Welcome to BigFish Offline Installer Downloader. To Download Games by their WrapID, create a file called wrapidlist.txt, place each wrapID on a separate line, then restart the script.
    Example:
    F123456L1
    F345678L1
    F654321L1
    
    Make sure that UAC (User Account Control) is disabled in Windows before continuing.
    
The program needs a timer value to run. It will be used for opening and closing the bigfish client to fetch download links.'

Recommendations:

2-3 for modern PCs built after 2015
5-10 for older pcs (2015 and older)

Maximum Allowed Value: 20

If you are getting errors, try a lower or higher value, depending on the value.

Type x to exit.''')

userinput = input('')

if userinput == 'x':
    print('Goodbye!')

while not validated_input(userinput):
    print('Timer value either too low, too high, or invalid input, please try again! \n')
    userinput = input('')

if userinput != 'x':
    timerval += float(userinput)
    while len(no_tries_by_wrapid) != 0:
        try:
            start_program(timerval)
        except:
            print("An unexpected error occurred. Either wrapID doesn't exist, or something went wrong.")
            break

if len(games_DL) >= 1 or len(games_not_DL) >= 1:
    print('\nTotal Downloaded: ' + calculate_size(total_downloaded) + '\n')
    print('Total Games Downloaded: ' + str(len(games_DL)) + '\n')
    print('WrapID             Game Name')
    for key, value in games_DL.items():
        print(key + (19 - len(key)) * ' ' + value[0] + '   [' + calculate_size(value[1]) + ']')
    print('\n Total Games Not Downloaded: ' + str(len(games_not_DL)) + '\n')
    print('WrapID             Game Name')
    for key, value in games_not_DL.items():
        print(key + (19 - len(key)) * ' ' + str(value))
    print(
        '\n Thank you for using kevinj93\'s BigFish Offline Installer. For full log, see bigFish_offlineInstaller_log.txt in main program folder.')

end = datetime.datetime.now()
app_end = '%d/%d/%d %.2d:%.2d:%.2d' % (end.day, end.month, end.year, end.hour, end.minute, end.second)

logfile = open('bigFish_offlineInstaller_log.txt', 'a', encoding='utf-16')

logfile.write('\nApplication Start: ' + app_start + '\n')
logfile.write('Application End: ' + app_end + '\n\n')
logfile.write('Total Downloaded: ' + calculate_size(total_downloaded) + '\n\n')
logfile.write('Total Games Downloaded: ' + str(len(games_DL)) + '\n\n')
logfile.write('WrapID             Game Name\n\n')

for key, value in games_DL.items():
    logfile.write(key + (19 - len(key)) * ' ' + value[0] + '   [' + calculate_size(value[1]) + '] \n')
logfile.write('\n')
logfile.write('Total Games Not Downloaded: ' + str(len(games_not_DL)) + '\n\n')
logfile.write('WrapID             Game Name\n\n')

for key, value in games_not_DL.items():
    logfile.write(key + (19 - len(key)) * ' ' + str(value) + '\n')

logfile.close()

print('Cleaning up leftovers ...')

for fid in failed_wrapid:
    for file in os.listdir():
        if os.path.isdir(fid):
            os.rmdir(fid)
for reg_file in os.listdir():  # temp reg files cleanup
    if '.reg' in reg_file:
        os.remove(reg_file)
for game in os.listdir():  # temp files cleanup
    if os.path.isdir(game):
        current_dir = './' + game + '/'
        for file in os.listdir(current_dir):
            if '.tmp' in file:
                os.remove(current_dir + file)

if 'DOWNLOADED' not in os.listdir():
    os.mkdir('DOWNLOADED')

for game in os.listdir():
    if os.path.isdir(game) and '-' in game:
        shutil.move(game, './DOWNLOADED/' + game)

if len(games_DL) > 0 and len(games_not_DL) == 0 and txtfile_in_dir:
    print('\n All the games have been downloaded successfully. Would you like to remove wrapidlist.txt? Type "y" for yes, "n" for no')
    rmv_answered = False
    while not rmv_answered:
        rmv_choice = input('')
        if rmv_choice == 'y':
            os.remove('wrapidlist.txt')
            rmv_answered = True
        elif rmv_choice == 'n':
            rmv_answered = True
        else:
            print('Invalid answer, please try again!')
elif len(games_DL) == 0 and regfailed_attempts >= 1:
    print('No Registry files have been read. Timer too low?! ')

print('\n Program Finished. Press any key to exit \n')
os.system('pause >nul')
