import requests
import time

def delete_messages(token, channel_id, user_id):
    '''
    Function to delete all client messages in a specific channel. Script by @z_h_ on discord.
    '''

    # Define the base URL for the Discord API
    base_url = 'https://discord.com/api/v9/channels/{}/messages'.format(channel_id)

    headers = {
        'Authorization': token
    }

    last_message_id = ''

    while True:
        if last_message_id:
            print(f'Requesting new block before {last_message_id}')
            response = requests.get(base_url, headers=headers, params={'limit': 100, 'before': last_message_id})
        else:
            response = requests.get(base_url, headers=headers, params={'limit': 100})

        if not response.json():
            break

        stuff = response.json()
        message_ids = [
            message['id']
            for message in stuff
            if message['author']['id'] == user_id
        ]

        print(f'Found {len(message_ids)} messages from user')

        for message_id in message_ids:
            try:
                if 'retry_after' in str(response.json()):
                    time.sleep(float(response.json()['retry_after']))
            except:
                pass
            start_time = time.time()
            response = requests.delete(base_url + '/' + message_id, headers=headers)
            if response.status_code == 204:
                print("Message ID {} deleted successfully.".format(message_id))
            else:
                print("Failed to delete message ID {}. Error: {}".format(message_id, response.json()))
            # Respect the rate limit
            sleep_time = 1.5
            wait = sleep_time - (time.time() - start_time)
            if wait > 0:
                time.sleep(wait)
            try:
                while 'retry_after' in str(response.json()):
                    try:
                        if 'retry_after' in str(response.json()):
                            time.sleep(float(response.json()['retry_after']))
                    except:
                        pass
                    start_time = time.time()
                    response = requests.delete(base_url + '/' + message_id, headers=headers)
                    if response.status_code == 204:
                        print("Message ID {} deleted successfully.".format(message_id))
                    else:
                        print("Failed to delete message ID {}. Error: {}".format(message_id, response.json()))
                    # Respect the rate limit
                    wait = sleep_time-(time.time()-start_time)
                    if wait > 0:
                        time.sleep(wait)
            except:
                pass

        last_message_id = stuff.pop()['id']


token = 'YOUR_ACCOUNT_TOKEN'
channel_id = 'THE_CHANNEL_ID'
user_id = 'YOUR_USER_ID'

delete_messages(token, channel_id, user_id)
