import urllib
import json
import requests
import googlemaps

google_key = "AIzaSyClQ-UNfzrPkI1mpHBHn2JFBSaN1eeeVw4"
gmaps = googlemaps.Client(key = google_key)

def search_message(store_name):
    address = store_name
    addurl = "https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false".format(google_key,address)
    addressReq = requests.get(addurl)
    addressDoc = addressReq.json()

    try:
        place_id = addressDoc["results"][0]["place_id"]
        detail_results = gmaps.place(place_id, language = "zh-tw")

        store_open = ""
        message = ""
        store_name = detail_results["result"]["name"]
        try:
            store_address = detail_results["result"]["formatted_address"]
        except:
            store_address = "Not Found"
        
        try:
            store_open_list = detail_results["result"]["opening_hours"]["weekday_text"]
            for open in store_open_list:
                store_open = store_open + "\n" + open
        except:
            store_open = "Not Found"

        try:
            store_phone = detail_results["result"]["formatted_phone_number"]
        except:
            store_phone = "Not Found"

        try:
            store_rating = detail_results["result"]["rating"]
        except:
            store_rating = "Not Found"

        try:
            store_price_number = detail_results["result"]["price_level"]
            if(store_price_number == 0):
                store_price = "便宜"
            elif(store_price_number == 1):
                store_price = "平價"
            elif(store_price_number == 2):
                store_price = "中價位"
            elif(store_price_number == 3):
                store_price = "高價位"
            elif(store_price_number == 4):
                store_price = "尊爵不凡價位"
        except:
            store_price = "Not Found"
            
        # try:
        #     store_website = detail_results["result"]["website"]
        # except:
        #     store_website = "Not Found"
        
        try:
            lat = detail_results["result"]["geometry"]["location"]["lat"]
            lng = detail_results["result"]["geometry"]["location"]["lng"]
            map_url = "https://www.google.com/maps/search/?api=1&query={},{}&query_place_id={}".format(lat, lng, place_id)
        except:
            map_url = "Not Found"
        message = "店名：" + store_name + "\n地址：" + store_address + "\n電話：" + store_phone + "\n營業時間：" + store_open + "\n價位：" + store_price + "\n評價：" + str(store_rating) + "(0~5)\n地圖：" + map_url
    except:
        message = "Not Found"
    
    return message

def search_photo(store_name):
    address = store_name
    addurl = "https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false".format(google_key,address)
    addressReq = requests.get(addurl)
    addressDoc = addressReq.json()

    try:
        place_id = addressDoc["results"][0]["place_id"]
        detail_results = gmaps.place(place_id, language = "zh-tw")
        photo_reference = detail_results["result"]["photos"][0]["photo_reference"]
        photo_width = detail_results["result"]["photos"][0]["width"]
        photo_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format(google_key, photo_reference, photo_width)
    except:
        photo_url = "https://www.bomb01.com/upload/news/original/c95e0d21eda50ebc16d5f8ef568f60a7.png"

    return photo_url

def search_address(store_name):
    address = store_name
    addurl = "https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false".format(google_key,address)
    addressReq = requests.get(addurl)
    addressDoc = addressReq.json()

    try:
        place_id = addressDoc["results"][0]["place_id"]
        detail_results = gmaps.place(place_id, language = "zh-tw")

        message = ""
        try:
            store_address = detail_results["result"]["formatted_address"]
        except:
            store_address = "Not Found"
        message = store_address
    except:
        message = "Not Found"
    
    return message