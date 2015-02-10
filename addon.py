import sys
import urllib
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import re

#Parsing html (stored locally)
from resources.lib import CBCParse
#Note, will need __init__.py
# getting addon object
my_addon = xbmcaddon.Addon('plugin.audio.CBCRadio')
#base url and handle of the addon
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
for arg in args:
    xbmc.log(arg)

xbmcplugin.setContent(addon_handle, 'songs')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
    
mode = args.get('mode',None)

if mode is None:
    url = build_url({'mode': 'folderEN', 'foldername': 'Folder One'})
    li = xbmcgui.ListItem('EN', iconImage='DefaultFolder.png')
    li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    #Plans to add a french directory, maybe for icaimusique.ca
    #url = build_url({'mode': 'folderFR', 'foldername': 'Folder Two'})
    #li = xbmcgui.ListItem('FR', iconImage='DefaultFolder.png')
    #li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

#Populates top-level directory with genre categories
elif mode[0] == 'folderEN':
    foldername = args['foldername'][0]
    categories = CBCParse.get_categories()
    for i in range(0,len(categories)):
        print categories[i]
        url = build_url({'mode': "category", 'foldername': categories[i]})
        li = xbmcgui.ListItem(categories[i], iconImage='DefaultFolder.png')
        li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

#Checks if the foldername is a category. If so, populates with all the stations in that category        
elif args['foldername'][0] in CBCParse.get_categories():
    xbmc.log("Entering category " + mode[0])
    foldername = args['foldername'][0]
    station_names = CBCParse.get_station_names_by_cat(foldername)
    for i in range(0,len(station_names)):
        playlist_url = CBCParse.get_station_url_by_station(station_names[i])
        playlist = urllib2.urlopen(playlist_url)
        playlist_text = playlist.read()
        url = re.findall(r"(?<=File1\=).*C",playlist_text)[0]
        li = xbmcgui.ListItem(station_names[i], iconImage='DefaultAudio.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
