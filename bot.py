import discord
import redis
from blockchain import Blockchain
import json
import os
client = discord.Client()
TOKEN="fdsinfsofnsdfon"
r = redis.Redis(host='localhost', port=6379, db=0)

try:
    os.remove("blockchain.json")
except:
    print("Cannot delete blockchain.json file")
file = open("blockchain.json", "x")
file.close()

init = {
    "blockchain": []
}
  
json_object = json.dumps(init, indent = 4)

with open("blockchain.json", "w") as outfile:
    outfile.write(json_object)

blockchain = Blockchain()
blockchain.update_blocks()

# Want users to be able to send Koins to each other
# Want users to be able to gain Koins through participation
# Users can send each other x amount of Koins each month (not added to their account) can be used as a reward for funny posts
# Prizes can be discord nitro, kurius merch, etc
# Transaction between users, monthly allowance, and prize redemption
# Find way to count Koins based on blockchain
# Have a store directly accessible via Discord (Transactions occur in the blockchain)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    num = 0

    if message.author == client.user:
        return
    else:
        if (r.get("total_messages_sent") == None):
            r.set("total_messages_sent", 1)
        else:
            number_of_messages = r.get('total_messages_sent')
            number_of_messages2 = int(number_of_messages.decode('utf-8')) + 1
            r.set("total_messages_sent", number_of_messages2)
            #Equivalent to total_messages_sent
    user_id = message.author.id
    split_message = message.content.split(" ")

    if (r.hget("messages_sent", user_id) == None):
        print(True)
        r.hset("messages_sent", user_id, 1)
    else:
        result = r.hget('messages_sent', user_id)
        result2 = int(result.decode('utf-8')) + 1
        r.hset("messages_sent", user_id, result2)
    
    messages_sent_by_user_string = r.hget('messages_sent', user_id)
    messages_sent_by_user_int = int(messages_sent_by_user_string.decode('utf-8'))

    if (messages_sent_by_user_int % 30 == 0):
        if (r.hget("number_of_koins", user_id) == None):
            r.hset('number_of_koins', user_id, 1)
            block_transaction = {"sender": str(client.user.name), "receiver": str(await client.fetch_user(message.author.id)), "amount": 1}
            blockchain.add_block(block_transaction)
            blockchain.update_blocks()
        else:
            result = r.hget('number_of_koins', user_id)
            result2 = int(result.decode('utf-8')) + 1
            r.hset("number_of_koins", user_id, result2)
            block_transaction = {"sender": str(client.user.name), "receiver": str(await client.fetch_user(message.author.id)), "amount": 1}
            blockchain.add_block(block_transaction)
            blockchain.update_blocks()

    total_messages_sent_string = r.get('total_messages_sent')
    total_messages_sent_int = int(total_messages_sent_string.decode('utf-8'))
    koins_array = r.hkeys("number_of_koins")

    if (total_messages_sent_int % 200 == 0):
        for c in range(len(koins_array)):
            key = str(koins_array[c].decode('utf-8'))
            if (r.hget("number_of_community_koins", key) == None):
                r.hset("number_of_community_koins", key, 30)
            else:
                r.hincrby("number_of_community_koins", key, 30)
            user_id = int(key)
            recipient_name = await client.fetch_user(user_id)
            block_transaction = {"sender": str(client.user.name), "receiver": str(recipient_name), "amount": 30}
            blockchain.add_block(block_transaction)
            blockchain.update_blocks()

    if split_message[0] == "$totalServerMessages":
        total_number_of_messages = r.get('total_messages_sent')
        total_number_of_messages_string = str(total_number_of_messages.decode('utf-8'))
        await message.channel.send('```' + total_number_of_messages_string + " messages have been sent!```")

    if split_message[0] == '$messages':
        messages_sent_by_specific_user = r.hget('message_sent', user_id)
        messages_sent_by_specific_user_string = str(messages_sent_by_user_string.decode('utf-8'))
        await message.channel.send('```You have sent ' + messages_sent_by_specific_user_string + " messages!```")
    
    if split_message[0] == '$showBlockchain':
        await message.channel.send(file=discord.File('blockchain.json'))
    
    if split_message[0] == '$giftCommunityKoins':
        amount_of_money = split_message[1]
        amount_of_money_int = int(amount_of_money)
        tagged_recipient = split_message[2]
        recipient_id =  tagged_recipient.replace("<@!","")
        final_recipient_id = recipient_id.replace(">","")
        final_recipient_id_num = int(final_recipient_id)
        sender_id = message.author.id
        amount_money_owned_by_sender = r.hget("number_of_community_koins", user_id)
        amount_money_owned_by_sender_int = int(amount_money_owned_by_sender.decode('utf-8'))
        recipient_name = await client.fetch_user(final_recipient_id_num)

        if (r.hget("number_of_community_koins", user_id) == None):
            await message.channel.send("You do not have any Community Koins in your name")

        elif final_recipient_id_num == sender_id:
            await message.channel.send('```You cannot gift yourself your own Community Koins!```')
        
        elif (amount_money_owned_by_sender_int < amount_of_money_int):
            await message.channel.send("You do not have enough Community Koins")
        
        elif (r.hget("number_of_koins",final_recipient_id_num) == None):
            r.hincrby("number_of_community_koins", sender_id, -amount_of_money_int)
            r.hset("number_of_koins", final_recipient_id_num, amount_of_money_int)
        else:
            r.hincrby("number_of_community_koins", sender_id, -amount_of_money_int)
            r.hincrby("number_of_koins", final_recipient_id_num, amount_of_money_int)
            block_transaction = {"sender": str(await client.fetch_user(message.author.id)), "receiver": str(recipient_name), "amount": amount_of_money}
            blockchain.add_block(block_transaction)
            blockchain.update_blocks()

    print(r.get("total_messages_sent"))
    print(r.hgetall("messages_sent"))
    print(r.hgetall("number_of_koins"))
    print(r.hgetall("number_of_community_koins"))
    # blockchain.print_blocks()

client.run(TOKEN)
# C:/Users/miste/AppData/Local/Programs/Python/Python39/python.exe c:/Users/miste/Downloads/KuriOS-main/KoinsBot/bot.py