import os
import CommonFunctions
common = CommonFunctions
common.plugin = "plugin.audio.CBCRadio-0.1.1"

#getting data to store station info
dir = os.path.dirname(__file__)
stations_path = os.path.join(dir,'../data/CBCStations.html')
station_list_file = open(stations_path,'r')  
station_list = file.read(station_list_file)
station_list_file.close()

def get_station_urls(category_titles):
    urls=[]
    for i in range(0,len(category_titles)):
        ret = common.parseDOM(station_list,"div",attrs = {"id":category_titles[i]})	
        ret2 = common.parseDOM(ret,"span",attrs = {"class":"streamUrl"})
        urls.append(common.parseDOM(ret2,"a",ret = "href"))

def get_station_names(category_titles):
    station_names=[]
    for i in range(0,len(category_titles)):
        #taking the block whose id matches the category
        ret = common.parseDOM(station_list,"div",attrs = {"id":category_titles[i]})
        station_names.append(common.parseDOM(ret,"a",attrs={"target":"_parent"}))
    return station_names
    
def get_categories():
    category_titles = common.parseDOM(station_list, "h3")
    for i in range(0,len(category_titles)):
        category_titles[i] = category_titles[i].encode('utf-8')
    return category_titles
    
def get_station_names_by_cat(category_name):
    station_names=[]
    ret = common.parseDOM(station_list,"div",attrs={"id":category_name})
    station_names=(common.parseDOM(ret,"a",attrs={"target":"_parent"}))
    for i in range(0,len(station_names)):
        station_names[i] = station_names[i].encode("utf-8")
    return station_names
    
def get_station_url_by_station(station_name):
    ret = [x for x in common.parseDOM(station_list,"li") if station_name in x]
    ret2 = common.parseDOM(ret,"span",attrs = {"class":"streamUrl"})
    link =(common.parseDOM(ret2,"a",ret = "href"))
    return link[0]
