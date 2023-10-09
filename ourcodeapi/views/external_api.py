from django.http import JsonResponse
import requests

def fetch_latest_news(request):
    base_url = "https://newsdata.io/api/1/news"
    api_key = "pub_30810f2dcad371f87365c23b883ded025f5e7"
    
   
    query_param = "tech"
    
    language = "en"

    
    full_url = f"{base_url}?apikey={api_key}&q={query_param}&language={language}"

    response = requests.get(full_url)
    print(response.text)
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": f"Failed to fetch the latest news. API responded with status code: {response.status_code}"}, status=500)
                        

