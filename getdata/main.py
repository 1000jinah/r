from fastapi import FastAPI
import requests
import time
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
AUTH = os.getenv("AUTH")
CLIENT_ID = os.getenv("CLIENT_ID")
TOONA_ID_VALUE = os.getenv("TOONA_ID_VALUE")

app = FastAPI()

headers = {
    'Authorization': AUTH,
    'Client-Id': CLIENT_ID,
}

ban_users = []
processed_logins = set()
get_id_data = []
toona_link_value = []

@app.get("/get_user_profiles", response_model=List[dict])
def get_user_profiles():
    user_profiles = []

    login_values = [
    'i_am_bona', 
    'saeyobim',
    'kangnanna',
    'zhuvely95',
    'wer1072',
    'foreversi1',
    'godsehee04',
    'appney',
    'bps1016',
    'miiing__', 
    'midany',
    'pikapikalove05',
    '0cheoli',
    'sonookiii',
    '62long',
    'leelate',
    'harukimharu', 
    'quo9807',
    'haemingwa',
    'lo_ve_u',
    'youchi0_0',
    'god_lita',
    'duswl1214',
    'inyoung1209',
    'tndus1532',
    'haumpah',
    'newna_ya',
    'p_tilda',
    'yokang_',
    'golaniyule0',
    'odimx26',
    'auddk_77',
    'kubin0515',
    'meuyou1',
    'yoon_froggy',
    'gyu_0227',
    'moon_yu_na',
    'yoonsan3',
    'dbwls04026',
    'noir1113',
    'haruzzxng',
    'mallang_peach_',
    'siru_cos27',
    'seul__lee', 
    'dedenzzang',
    '0ijeonghaha97',
    'youdahi_',
    'rang_nabi',
    'einaholic',
    'mymai_s2',
    'olaf3728',
    'ayo_0410',
    'mintcandy25',
    'starryday7',
    'lluchiaa',
    'hwho0',
    'ao_oavv',
    'hanasooong',
    'truewater_',
    'jojohaeun',
    'sugaluna_vov',
    'l2003001',
    'nyeongbam',
    '100yang2',
    'anyaa030',
    'llullulu0',
    'dearmyx_',
    'ne_byura',
    'ddurori',
    'eunobbonno',
    'mingcho0514',
    'jin1130',
    'ddo__youn',
    'skaalswjd1',
    'immyomi',
    'suayun999',
    'chaeichaei',
    're_zero_kara',
    'yumyum1123',
    'hyellkang',
    '2lyn_98',
    'world1104',
    'minjeng415',
    'jnn0213',
    'dayul010',
    'woojungx4',
    'd0zzang',
    'melonell',
    'juzzing0112',
    'yomicoskr',
    'mazza0413',
    'dadan1224',
    'seoahtv_',
    'jujuplease',
    'boss_julie',
    'ecobs3478',
    'ddil__bbang',
    'lovee_2',
    'leeae_',
    'dyangyi',
    'luvuhiki',
    'gobacksoon',
    'bandarling',
    'akikxo',
    'bbang_eu',
    'woohankyung',
    'berry0314',
    'yu2bee',
    'magenta62',
    'summerjoo_',
    'misolight1004',
    'myyondi',
    'yeo_ul_',
    'jaetyweety',
    'mia_go612',
    'weet1114',
    '156kiki',
    '0due_',
    'seo_hina',
    'love0_0uuuu',
    'holickk',
    'hapd02',
    'awesomee_eee',
    'luvming01',
    'tocomo_818',
    'kuro_hime_mi',
    'yueuni0_0',
    'yuwol_92',
    'h_seha',
    'glgle6776',
    'haring77',
    'eun020125',
    'chodan_',
    ]

    for i, login in enumerate(login_values, 1):
        reqs = requests.get(f'https://api.twitch.tv/helix/users?login={login}', headers=headers)

        if reqs.status_code == 200:
            try:
                user_info = reqs.json()['data'][0]
                tw_personal_id = user_info['id']
                display_name = user_info['display_name']
                login = user_info['login']
                profile_image_url = user_info['profile_image_url']

                user_profiles.append({'id': tw_personal_id, 'display_name': display_name, 'login': login, 'profile_image_url': profile_image_url})
            except IndexError:
                print(f"No data found for user: {login}")
                ban_users.append(login)
        else:
            print(f"Error fetching data. (User: {login})")

    return user_profiles


@app.get("/get_banned_users", response_model=List[str])
def get_banned_users():
    return ban_users


@app.get("/process_set_link_data", response_model=List[dict])
def process_set_link_data():
    link_data = []

    # Get user profiles and use their id values as logins
    user_profiles = get_user_profiles()

    # Exclude banned users from logins
    logins = {profile['id'] for profile in user_profiles if profile['login'] not in ban_users}

    # 이미 저장한 login 값을 추적하기 위한 집합
    processed_logins = set()

    # 각 login 값에 대한 GraphQL 쿼리를 실행하고 결과를 저장합니다.
    for login in logins:
        # 이미 저장한 경우 스킵
        if login in processed_logins:
            continue

        response = requests.post(
            'https://gql.twitch.tv/gql',
            headers={'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'},
            json={
                "operationName": "ChannelPanels",
                "extensions": {
                    "persistedQuery": {
                        "sha256Hash": "c388999b5fcd8063deafc7f7ad32ebd1cce3d94953c20bf96cffeef643327322",
                        "version": 1
                    }
                },
                "variables": {"id": login}
            }
        )

        data = response.json()

        if "data" in data and "user" in data["data"] and data["data"]["user"] and "panels" in data["data"]["user"]:
            panels_info = data["data"]["user"]["panels"]

            for panel in panels_info:
                id_value = panel.get('id', '')  # 'id' 값을 가져옴

                if id_value not in processed_logins:
                    processed_logins.add(id_value)
                    # Extract 'toon.at/donate/' and "," values from the linkURL
                    link_url = panel.get('linkURL', '')
                    if 'toon.at/donate/' in link_url:
                        start_index = link_url.find('toon.at/donate/') + len('toon.at/donate/')
                        end_index = link_url.find('"', start_index)
                        extracted_value = link_url[start_index:end_index]
                        toona_link_value.append({'id': id_value, 'linkURL': extracted_value, 'type': 'link'})
                    # Add the processed login
                    link_data.append({'login': login, 'panel': panel})  # login과 'id' 값을 저장

        else:
            print(f"User with id '{login}' does not have panel information.")

    return link_data

@app.get("/process_user_data", response_model=List[dict])
def process_user_data():
    # Read processed logins from get_id_data
    for row in get_id_data:
        processed_logins.add(row['login'])

    # Read logins from user_profile.csv
    logins = []

    for row in get_user_profiles():
        logins.append(row['login'])

    # Process each login
    for index, login in enumerate(logins, start=1):
        if login in processed_logins:
            print(f"[{index}/{len(logins)}] User with login '{login}' is already processed. Skipping...")
            continue

        response = requests.post(
            "https://gql.twitch.tv/gql",
            json=[
                {
                    "query": f"""
                        query{{
                            user(login: "{login}"){{
                                id,
                                login,
                                displayName,
                                channel{{
                                    socialMedias{{
                                        url,
                                        title
                                    }}
                                }}
                            }}
                        }}
                    """
                },
            ],
            headers={'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
        )
        time.sleep(0.1)
        data = response.json()

        if "data" in data[0] and "user" in data[0]["data"] and data[0]["data"]["user"] and "channel" in data[0]["data"]["user"]:
            user_info = data[0]["data"]["user"]

            # Append data to get_id_data list
            if user_info["channel"]["socialMedias"]:
                for social_media in user_info["channel"]["socialMedias"]:
                    # Extract 'toon.at/donate/' and "," values from the url
                    user_url = social_media.get('url', '')
                    if 'toon.at/donate/' in user_url:
                        start_index = user_url.find('toon.at/donate/') + len('toon.at/donate/')
                        end_index = user_url.find('"', start_index)
                        extracted_value = user_url[start_index:end_index]
                        toona_link_value.append({'id': user_info["id"], 'url': extracted_value, 'type': 'url'})
                    get_id_data.append({'id': user_info["id"], 'login': user_info["login"], 'displayName': user_info["displayName"],
                                        'url': social_media["url"], 'title': social_media["title"]})
            else:
                # Assign "null" if socialMedias is empty
                get_id_data.append({'id': user_info["id"], 'login': user_info["login"], 'displayName': user_info["displayName"],
                                    'url': 'null', 'title': 'null'})

            processed_logins.add(login)  # Add processed logins
            print(f"[{index}/{len(logins)}] Processed user with login '{login}'.")
        else:
            print(f"[{index}/{len(logins)}] User with login '{login}' does not have channel information.")

    return get_id_data

@app.get("/toon_roulette_data", response_model=List[dict])
def get_toon_roulette_data():
    link_data = toon_donate_data()

    toon_roulette_data = []

    for entry in link_data:
        url = f'https://toon.at/dapi/donate/{entry["url"]}'

        while True:  # Continue attempting until successful
            response = requests.get(url)
            
            # Check if we are on the expected page
            if 'dapi/donate' in response.url:
                break

            # Add cookie and wait

            response = requests.get(url, cookies={'__toonation_session_id__': TOONA_ID_VALUE})
        
        # Process the response, assuming it's JSON data
        try:
            data = response.json()
            toon_roulette_data.append(data)
        except ValueError as e:
            print(f"Error parsing JSON: {e}")

    return toon_roulette_data

if __name__ == "__main__":
    import uvicorn

    # Run FastAPI
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")