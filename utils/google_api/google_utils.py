def get_google_api_key():
    with open('/etc/google_api_key.txt', 'r') as f:
        return f.read().strip()