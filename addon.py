import sys
import xbmcgui
import xbmcplugin

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'music')

url = 'http://playerservices.streamtheworld.com/pls/CBC_R1_OTT_H.pls'
li = xbmc.ListItem('CBC Radio One',iconImage='CBCLogo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
