import requests

def status_detail(kurir, no_resi):
  api_url = f"https://api.binderbyte.com/v1/track?api_key=7355af5dd29cf5cf36854c280018d6faed94c4990b9430c57feb0c31b9119d02&courier={kurir}&awb={no_resi}"
  response = requests.get(api_url)
  if response.status_code == 200:
    data = response.json()
    datas = data["data"]["summary"]
    detail_data = data["data"]["detail"]
    #awb = datas["awb"]
    courier = datas["courier"]
    service = datas["service"]
    status = datas["status"]
    date = datas["date"]
    desc = datas["desc"]
    weight = datas["weight"]
    
    origin = detail_data["origin"]
    destination = detail_data["destination"]
    shipper = detail_data["shipper"]
    receiver = detail_data["receiver"]
      
    return (
      courier, service,
      status, date, desc,
      weight, origin, destination,
      shipper, receiver
    )
    
  else:
    return "data tidak ditemukan"

def get_history(kurir, no_resi):
  api_url = f"https://api.binderbyte.com/v1/track?api_key=7355af5dd29cf5cf36854c280018d6faed94c4990b9430c57feb0c31b9119d02&courier={kurir}&awb={no_resi}"
  response = requests.get(api_url)
  
  if response.status_code == 200:
    r_data = response.json()
    history = r_data.get("data")["history"]
    last_history = history[0]
    
    return last_history["desc"]