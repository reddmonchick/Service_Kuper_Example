import pytest
import tls_client

@pytest.mark.skip
def test_sync():
    session = tls_client.Session(

        client_identifier="chrome_120",

        random_tls_extension_order=True

    )

    params = {
            'lat': '55.035706',
            'lon': '82.896166',
            'q': 'Молоко',
        }

    headers = {
            'client-id': 'KuperAndroid',
            'client-token': '241f3ea68b8ca03f60c4111b9f39c63d',
            'client-ver': '15.3.40',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'client-bundleid': 'ru.instamart',
            'api-version': '2.2',
            'cache-control': 'no-store',
            'content-type': 'application/json',
            'anonymousid': '03d2c216ac476531',
            'screenname': 'MultiRetailSearch',
        }

    response = session.get('https://api.kuper.ru/v2/multisearches', params=params, headers=headers)

    print(response)
    assert response.status_code == 200
