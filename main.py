import requests
import json

def retrieve_messages(channelid, filename, number_of_messages="all", authorization=None):
    with open(f"{filename}", "w") as f:
        num = 0
        limit = 100

        headers = {
            'authorization': f'{authorization}'
        }

        last_message_id = None
        messages = []
        exceeded = False
        last = ""

        while True:
            query_parameters = f'limit={limit}'
            if last_message_id is not None:
                query_parameters += f'&before={last_message_id}'

            r = requests.get(
                f'https://discord.com/api/v9/channels/{channelid}/messages?{query_parameters}', headers=headers
                )
            jsonn = json.loads(r.text)
            if len(jsonn) == 0:
                break
            
            
            
            for value in jsonn:
                if number_of_messages != "all":
                    if num >= number_of_messages:
                        exceeded = True
                        break
                username = value["author"]["username"]
                content = value["content"]
                timestamp = value["timestamp"][:10]
                if content != "":
                    if username == last:
                        messages.append((f'[{timestamp}] {username}: {content}\n'))
                    else:
                        last = username
                        messages.append((f'[{timestamp}] {username}: {content}\n\n'))


                last_message_id = value['id']
                num=num+1
                print(num, "messages written")
            if exceeded:
                break

        messages = messages[::-1]
        for message in messages:
            f.write(message)
        print("done")
        

def main():
    channel_id = input("input channel id: ")
    authorization = input("input authorization token: ")
    how_many = input("how many messages would you like to write (write \"all\" for all): ")
    try:
        how_many = int(how_many) if how_many != "all" else "all"
    except:
        print("enter an integer or all")
    file_name = input("what would you like to name your file (.txt): ")
    try:
        retrieve_messages(channel_id, file_name, how_many, authorization)
    except:
        print("something went wrong try again")



if __name__ == "__main__":
    main()


