import sys
import urllib
import urllib2
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import re

#Parsing html (stored locally)
from resources.lib import CBCParse, CBCJsonParser
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
    url = build_url({'mode': 'Radio1', 'foldername': 'Folder One'})
    li = xbmcgui.ListItem('Radio1', iconImage='DefaultFolder.png')
    li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'Radio2', 'foldername': 'Folder Two'})
    li = xbmcgui.ListItem('Radio2', iconImage='DefaultFolder.png')
    li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

# Populates directory with region links for Radio 1
elif mode[0] == 'Radio1':
    foldername = args['foldername'][0]
    regions = CBCJsonParser.get_regions('radio1')
    for region in regions:
        url = build_url({'mode': 'r1_regions', 'foldername': region})
        li = xbmcgui.ListItem(region, iconImage='DefaultFolder.png')
        li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

# Populates directory with region links for Radio 2
elif mode[0] == 'Radio2':
    foldername = args['foldername'][0]
    regions = CBCJsonParser.get_regions('radio2')
    for region in regions:
        playlist_url = CBCJsonParser.get_R2_streams(region)
        url = CBCJsonParser.parse_pls(playlist_url)
        li = xbmcgui.ListItem(region, iconImage='DefaultFolder.png')
        li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'Radio3':
    pass

elif mode[0] == 'Sonica':
    pass

# Create list items and URLs for Radio 1
elif mode[0] == 'r1_regions':
    region = args['foldername'][0].decode('utf-8')

    aac_playlist_url, mp3_playlist_url = CBCJsonParser.get_R1_streams(region)
    aac_stream_url = CBCJsonParser.parse_pls(aac_playlist_url)
    mp3_stream_url = CBCJsonParser.parse_pls(mp3_playlist_url)

    aac_li = xbmcgui.ListItem(region + ' - High Quality (AAC)', iconImage='DefaultAudio.png')
    mp3_li = xbmcgui.ListItem(region + ' - Low Quality (MP3)', iconImage='DefaultAudio.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=aac_stream_url, listitem=aac_li)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=mp3_stream_url, listitem=mp3_li)
    xbmcplugin.endOfDirectory(addon_handle)

# TODO. Add Soncica and Radio 3
