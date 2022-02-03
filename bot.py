import discord
from db import message_database, koins_database, community_koins_database, total_messages_sent
from blockchain import Blockchain
import json
import os
client = discord.Client()
TOKEN="OTM0MTIwMzY5NDY2NTMxODUw.YerdYw.vl7K9qhD9GbOMJFaWKtWSfOjeKo"

try:
    os.remove("blockchain.json")
except:
    print("Cannot delete blockchain.json file")
file = open("blockchain.json", "x")
file.close()

data2 = {
    "blockchain": []
}
  
json_object = json.dumps(data2, indent = 4)

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    num = 0

    if message.author == client.user:
        return
    else:
        total_messages_sent.append("")
    split_message = message.content.split(" ")

    if len(message_database) == 0:
        new_user = {message.author.id: 1}
        message_database.append(new_user)
    else:
        num2 = 0
        for i in range(len(message_database)):
            if str(message_database[i].keys()) == "dict_keys([" + str(message.author.id) + "])":
                message_database[i][message.author.id] += 1
                num2 = 1
        if num2 != 1:
            new_user = {message.author.id: 1}
            message_database.append(new_user)
    
    for i in range(len(message_database)):
        if str(message_database[i].keys()) == "dict_keys([" + str(message.author.id) + "])":
            if message_database[i][message.author.id] % 1 == 0: # For every 30 messages sent by the user, the user will receive one Koins
                if len(koins_database) == 0:
                    new_user = {message.author.id: 1}
                    koins_database.append(new_user)
                    block_transaction = {"sender": str(client.user.name), "receiver": str(await client.fetch_user(message.author.id)), "amount": 1}
                    blockchain.add_block(block_transaction)
                    blockchain.update_blocks()
                else:
                    num3 = 0
                    for k in range(len(koins_database)):
                        if str(koins_database[k].keys()) == "dict_keys([" + str(message.author.id) + "])":
                            # ADDS KOINS
                            block_transaction = {"sender": str(client.user.name), "receiver": str(await client.fetch_user(message.author.id)), "amount": 1}
                            blockchain.add_block(block_transaction)
                            num3 = 1
                            koins_database[k][message.author.id] += 1
                            blockchain.update_blocks()
                    if num3 != 1:
                        block_transaction = {"sender": str(client.user.name), "receiver": str(await client.fetch_user(message.author.id)), "amount": 1}
                        blockchain.add_block(block_transaction)
                        new_user = {message.author.id: 1}
                        koins_database.append(new_user)
                        blockchain.update_blocks()

    if len(total_messages_sent) % 1 == 0: # For every 500 messages sent by users, each user will receive 30 Community Koins
        for i in range(len(message_database)):
            key = str(message_database[i].keys())
            key2 = key.replace("dict_keys([", "")
            key3 = key2.replace("])", "")
            key4 = key3.replace(",", "")
            key4_num = int(key4)
            num7 = 0
            for c in range(len(community_koins_database)):
                if str(message_database[c].keys()) == "dict_keys([" + key4 + "])":
                    community_koins_database[c][key4_num] += 30
                    recipient_name = await client.fetch_user(key4_num)
                    block_transaction = {"sender": str(client.user.name), "receiver": str(recipient_name), "amount": 30}
                    blockchain.add_block(block_transaction)
                    blockchain.update_blocks()
                    num7 = 1
            if num7 != 1:
                new_user = {key4_num: 30}
                community_koins_database.append(new_user)
                recipient_name = await client.fetch_user(key4_num)
                block_transaction = {"sender": str(client.user.name), "receiver": str(recipient_name), "amount": 30}
                blockchain.add_block(block_transaction)
                blockchain.update_blocks()

    if split_message[0] == '$Koins':
        num5 = 0
        for k in range(len(koins_database)):
                if str(koins_database[k].keys()) == "dict_keys([" + str(message.author.id) + "])":
                    account_value =  koins_database[k][message.author.id]
                    num5 = 1
        if num5 != 1:
            account_value = 0
        await message.channel.send('```You have ' + str(account_value)  + " Koins!```")

    if split_message[0] == "$TotalServerMessages":
        await message.channel.send('```' + str(len(total_messages_sent)) + " messages have been sent!```")

    if split_message[0] == '$Messages':
        num6 = 0
        for i in range(len(message_database)):
            if str(message_database[i].keys()) == "dict_keys([" + str(message.author.id) + "])":
                messages_sent = message_database[i][message.author.id]
                num6 = 1
        if num6 != 1:
            messages_sent = 1
        await message.channel.send('```You have sent ' + str(messages_sent) + " messages!```")
    
    if split_message[0] == '$ShowBlockchain':
        await message.channel.send(file=discord.File('blockchain.json'))
    
    if split_message[0] == '$GiftKoins':
        num8 = 0
        amount_of_money = split_message[1]
        amount_of_money_num = int(amount_of_money)
        tagged_recipient = split_message[2]
        recipient_id =  tagged_recipient.replace("<@!","")
        final_recipient_id = recipient_id.replace(">","")
        final_recipient_id_num = int(final_recipient_id)
        recipient_name = await client.fetch_user(final_recipient_id_num)
        sender_id = message.author.id
        if final_recipient_id_num == sender_id:
            await message.channel.send('```You cannot gift yourself your own Koins!```')
            num8 = 1
        for k in range(len(koins_database)):
                        if str(koins_database[k].keys()) == "dict_keys([" + str(message.author.id) + "])":
                            account_value =  koins_database[k][message.author.id]
                            if account_value < amount_of_money_num:
                                await message.channel.send("```You don't have enough Koins!```")
                                num8 = 1
                            else:
                                koins_database[k][message.author.id] -= amount_of_money_num
        if len(koins_database) == 0 and num8 == 0:
            new_user = {final_recipient_id_num: amount_of_money_num}
            koins_database.append(new_user)
            block_transaction = {"sender": str(await client.fetch_user(message.author.id)), "receiver": str(recipient_name), "amount": amount_of_money}
            blockchain.add_block(block_transaction)
            blockchain.update_blocks()     
        elif num8 == 0:
            for k in range(len(koins_database)):
                if str(koins_database[k].keys()) == "dict_keys([" + str(final_recipient_id) + "])":
                    block_transaction = {"sender": str(await client.fetch_user(message.author.id)), "receiver": str(recipient_name), "amount": amount_of_money}
                    blockchain.add_block(block_transaction)
                    koins_database[k][final_recipient_id_num] += amount_of_money_num
                    blockchain.update_blocks()
                    num = 1
            if num != 1:
                block_transaction = {"sender": str(await client.fetch_user(message.author.id)), "receiver": str(recipient_name), "amount": amount_of_money}
                blockchain.add_block(block_transaction)
                new_user = {final_recipient_id_num: amount_of_money_num}
                koins_database.append(new_user)
                blockchain.update_blocks()
                num = 0
        if num8 == 0:
            await message.channel.send('```You have gifted ' + str(recipient_name) + ' ' + amount_of_money + ' Koins!```')
    
    if split_message[0] == '$GiftCommunityKoins':
        num9 = 0
        amount_of_money = split_message[1]
        amount_of_money_num = int(amount_of_money)
        tagged_recipient = split_message[2]
        recipient_id =  tagged_recipient.replace("<@!","")
        final_recipient_id = recipient_id.replace(">","")
        final_recipient_id_num = int(final_recipient_id)
        recipient_name = await client.fetch_user(final_recipient_id_num)
        sender_id = message.author.id
        if final_recipient_id_num == sender_id:
            await message.channel.send('```You cannot gift yourself your own Koins!```')
            num9 = 1
        for k in range(len(community_koins_database)):
                if str(community_koins_database[k].keys()) == "dict_keys([" + str(message.author.id) + "])":
                    account_value =  community_koins_database[k][message.author.id]
                    if account_value < amount_of_money_num:
                        await message.channel.send("```You don't have enough Koins!```")
                        num9 = 1
                    else:
                        community_koins_database[k][message.author.id] -= amount_of_money_num
        if len(community_koins_database) == 0 and num9 == 0:
            new_user = {final_recipient_id_num: amount_of_money_num}
            koins_database.append(new_user)
            block_transaction = {"sender": str(await client.fetch_user(message.author.id)), "receiver": str(recipient_name), "amount": amount_of_money}
            blockchain.add_block(block_transaction)
            blockchain.update_blocks()              
        elif num9 == 0:
            for k in range(len(community_koins_database)):
                if str(community_koins_database[k].keys()) == "dict_keys([" + str(final_recipient_id) + "])":
                    block_transaction = {"sender": str(await client.fetch_user(message.author.id)), "receiver": str(recipient_name), "amount": amount_of_money}
                    blockchain.add_block(block_transaction)
                    koins_database[k][final_recipient_id_num] += amount_of_money_num
                    blockchain.update_blocks()
                    num = 1
            if num != 1:
                block_transaction = {"sender": str(await client.fetch_user(message.author.id)), "receiver": str(recipient_name), "amount": amount_of_money}
                blockchain.add_block(block_transaction)
                new_user = {final_recipient_id_num: amount_of_money_num}
                koins_database.append(new_user)
                blockchain.update_blocks()
                num = 0
        if num9 == 0:
            await message.channel.send('```You have gifted ' + str(recipient_name) + ' ' + amount_of_money + ' Koins!```')


    print(len(total_messages_sent))
    print(message_database)
    print(koins_database)
    print(community_koins_database)
    # blockchain.print_blocks()

client.run(TOKEN)
