import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib import CBCParse
#Note, will need __init__.py
#sys.path.append(os.path.join(_addon_path, 'resources', 'lib'))
#import CBCParse
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
    
def createListing():
    listing = []
    listing.append(('Radio One Ottawa','http://playerservices.streamtheworld.com/pls/CBC_R1_OTT_H.pls','Talk'))
    listing.append(('Radio Two Ottawa','http://2073.live.streamtheworld.com/CBC_R2_TOR_H','Music Radio'))
    return listing
    #listing.append("")
    
def populateDirectory(listing):
    for item in listing:
        li = xbmcgui.ListItem(item[0],iconImage=my_addon.getAddonInfo('icon'))
        li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
        #li.setInfo('music',{'genre':item[2]})
        xbmcplugin.addDirectoryItem(handle=addon_handle,url=item[1],listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)    
    
mode = args.get('mode',None)

if mode is None:
    url = build_url({'mode': 'folderEN', 'foldername': 'Folder One'})
    li = xbmcgui.ListItem('EN', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'mode': 'folderFR', 'foldername': 'Folder Two'})
    li = xbmcgui.ListItem('FR', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'folderEN':
    foldername = args['foldername'][0]
    categories = CBCParse.get_categories()
    for i in range(0,len(categories)):
        print categories[i]
        url = build_url({'mode': "category", 'foldername': categories[i]})
        li = xbmcgui.ListItem(categories[i], iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
        #for station in station_names[i]
        #li = xbmcgui.ListItem(station)
        
elif args['foldername'][0] in CBCParse.get_categories():
    xbmc.log("Entering category " + mode[0])
    foldername = args['foldername'][0]
    station_names = CBCParse.get_station_names_by_cat(foldername)
    for i in range(0,len(station_names)):
        url = CBCParse.get_station_url_by_station(station_names[i])
        li = xbmcgui.ListItem(station_names[i], iconImage='DefaultAudio.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


#populateDirectory(createListing())

#elif mode[0]=='folder_FR':
#    foldername = args['foldername'][0]
#    url = build_url({'mode': 'folder', 'foldername': 'CBC Radio Numbers'})
#    li = xbmcgui.ListItem('CBC Radio Numbers', iconImage=my_addon.getAddonInfo('icon'))
#    li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
#    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
#    xbmcplugin.endOfDirectory(addon_handle)



#elif mode[0] == 'folderEN':
#    foldername = args['foldername'][0]
#    listing = []
#    listing.append(('Radio One Ottawa','http://playerservices.streamtheworld.com/pls/CBC_R1_OTT_H.pls','Talk'))
#    listing.append(('Radio Two Ottawa','http://playerservices.streamtheworld.com/pls/CBC_R2_TOR_H.pls','Music Radio'))
#    for item in listing:
#        li = xbmcgui.ListItem(item[0])#iconImage=my_addon.getAddonInfo('icon'))
#        li.setProperty('fanart_image',my_addon.getAddonInfo('fanart'))
#        li.setInfo('music',{'genre':item[2]})
#        xbmcplugin.addDirectoryItem(handle=addon_handle,url=item[1],listitem=li)
#        
#    xbmcplugin.endOfDirectory(addon_handle)

