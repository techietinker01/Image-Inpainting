import requests

try:
    r = requests.get('http://127.0.0.1:5000/')
    print('GET / status', r.status_code)
    print('Snippet:', r.text[:400])
except Exception as e:
    print('Error fetching /:', e)

for path in ['main.js', 'styles.css']:
    try:
        r = requests.get(f'http://127.0.0.1:5000/static/{path}')
        print(f'{path} status', r.status_code, 'len', len(r.text))
    except Exception as e:
        print(f'Error fetching /static/{path}:', e)
