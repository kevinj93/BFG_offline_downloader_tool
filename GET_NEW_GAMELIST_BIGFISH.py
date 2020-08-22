import urllib.request

bf_handle = urllib.request.Request('https://www.bigfishgames.com/download-games/new-releases.html', data=None, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
file_bytes = urllib.request.urlopen(bf_handle).readlines()
file = []
for line in file_bytes:
    file.append(line.decode('utf-8'))

#file = open('New PC Games _ Big Fish.html', 'r', encoding='utf8').readlines()

links = []

for line in file:
    if len(links) == 44:
        break
    if 'top10' in line:
        break
    if '?pc' in line:
        startidx = line.index('<a href="')+9
        endidx = line.index('?pc"')+3
        if line[startidx:endidx] not in links:
            links.append(line[startidx:endidx])
#print('Last 44 Released Games on BigFish: \n')

new_gamelist = []

for link in links:
    split_link = link.split('/')
    wrapid = split_link[4]
    gamename = split_link[5].replace('-', ' ').title()
    if gamename.endswith(' Ce'):
        new_gamelist.append(wrapid + 'T1L1 - ' + gamename[:-3] + ' Collector\'s Edition\n')
    else:
        new_gamelist.append(wrapid + 'T1L1 - ' + gamename+'\n')

writefile = open('Last_44_games_BigFish.txt', 'w', encoding='utf8')
for game in new_gamelist:
    writefile.write(game)
writefile.close()
