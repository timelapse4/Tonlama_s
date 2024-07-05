import requests
import threading
import time
import locale

# Dictionary to store total coins received for each token
total_coins_per_token = {}

def send_request(token):
    url = 'https://lama-backend-clan.onrender.com/user/paidspin'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,en-US;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.tonlama.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.tonlama.com/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AG Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.71 Mobile Safari/537.36',
        'x-requested-with': 'org.telegram.messenger.web'
    }
    data = '{"user_id":6244090559}'
    response = requests.post(url, headers=headers, data=data)
    if 'spin' in response.json():
        spin_result = response.json()['spin']
        if spin_result == 0:
            coins_received = 50000
        elif spin_result == 1:
            coins_received = 150000
        elif spin_result == 2:
            coins_received = 200000
        elif spin_result == 3:
            coins_received = 250000
        elif spin_result == 4:
            coins_received = 500000
        elif spin_result == 5:
            coins_received = 50000
        else:
            coins_received = 0  # Handle unexpected spin results
        
        total_coins_per_token[token] = total_coins_per_token.get(token, 0) + coins_received
        print(f"{token}: You got {coins_received} Coin")

def process_token_in_batches(token, batch_size=100):
    threads = []
    for _ in range(batch_size):
        thread = threading.Thread(target=send_request, args=(token,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()  # Wait for all threads in the batch to finish

# Infinite loop to process tokens
while True:
    token = "tonlama"  # Replace with the actual token you want to use
    process_token_in_batches(token, batch_size=1000)

    # Print total coins received for the token
    formatted_coins = "{:,}".format(total_coins_per_token[token])  # Format with commas every three digits
    print(f"{token}: {formatted_coins}")

    # Calculate and print overall total coins received
    overall_total_coins = sum(total_coins_per_token.values())
    formatted_overall_total = "{:,}".format(overall_total_coins)  # Format overall total with commas
    print(f"Overall total coins received: {formatted_overall_total}")

    time.sleep(1)  # Optional: Add a delay to avoid overwhelming the server