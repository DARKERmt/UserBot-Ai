from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import MessageEntitySpoiler
from telethon.extensions import markdown
from telethon import types
import gemini as ai
from telethon.sync import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator,InputPeerUser
from pytgcalls import GroupCallFactory
from youtube_search import YoutubeSearch
import os
import asyncio

# Replace the values below with your own API credentials
api_id = 'Api_id'
api_hash = 'Api_hash'
phone_number = 'Your_number'
session_file = 'session'
User_id = your_id

# Create a new TelegramClient instance
client = TelegramClient(session_file, api_id, api_hash)

# Function to handle incoming messages
@client.on(events.NewMessage(pattern='!ask'))
async def handle_message(event):
    if event.sender_id == User_id:
        message = event.message.message
        if len(message.split()) > 1:
            response = ' '.join(message.split()[1:])
            ans = ai.text_ai(response)
            await event.respond(ans)
        else:
            await event.respond("Please ask me a question.")
    else:
        await event.respond("Sorry, you are not authorized to use this command.")

# Function to handle /members command
@client.on(events.NewMessage(pattern='!members'))
async def members_list(event):
    if event.sender_id == User_id:
        try:
            channel_username = event.message.text.split('@')[1]
            entity = await client.get_entity(channel_username)
            members = await client.get_participants(entity)
            member_list_str = '\n'.join([f'{member.id}: {member.first_name} {member.last_name}' for member in members])
            await event.respond(member_list_str)
        except Exception as e:
            await event.respond(f"Error: {str(e)}")
    else:
        await event.respond("Sorry, you are not authorized to use this command.")
        

# Function to handle /memlist command
@client.on(events.NewMessage(pattern='!memlist'))        
async def get_members(event):
    if event.sender_id == User_id:
        try:
            chat = event.message.to_dict().get('chat')
            if chat and chat.get('username'):
                channel_username = chat.get('username')
                entity = await client.get_entity(channel_username)
                participants = await client.get_participants(entity)
                member_info = '\n'.join([f'{participant.id}: {participant.first_name} {participant.last_name}' for participant in participants])
                await event.respond(member_info)
            else:
                await event.respond("Couldn't retrieve chat information.")
        except Exception as e:
            await event.respond(f"Error: {str(e)}")
    else:
        await event.respond("Sorry, you are not authorized to use this command.")


# user information get
        
@client.on(events.NewMessage(pattern='!user'))
async def get_user_info(event):
    if event.sender_id == User_id:
        try:
            if event.is_reply:
                user_id = (await event.get_reply_message()).from_id
            else:
                user_id = event.message.from_id
                
            user = await client.get_entity(user_id)
            info = f"First name: {user.first_name} \nLast Name: {user.last_name}\nUsername: {user.username}\nID: {user.id}"
            await event.respond(info)
        except Exception as e:
            await event.respond(f"Error: {str(e)}")
    else:
        await event.respond("Sorry, you are not authorized to use this command.")
        
        
        


# save any type of media
@client.on(events.NewMessage(pattern=r'!save'))
async def save_image(event):
    if event.sender_id == User_id:
        try:
            # Check if the message is a reply to another message
            if event.message.reply_to:
                replied_msg = await event.message.get_reply_message()
                # Check if the replied message contains an image
                if replied_msg.media and hasattr(replied_msg.media, 'photo'):
                    # Download the media (photo)
                    result = await replied_msg.download_media()
                    # Send the image to the current chat
                    # await client.send_file(event.chat_id, result, caption="Elisa can do bro..")
                    # Send the downloaded media to the saved chat with a caption
                    await client.send_file("me", result, caption="Elisa can do bro..")
                else:
                    # If no image is found in the replied message, reply with a message indicating so
                    await event.reply("No image found to save.")
            else:
                # If the message is not a reply, instruct the user to reply to an image message
                await event.reply("Please reply to an image message with '!save' to save it.")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    else:
        await event.respond("Sorry, you are not authorized to use this command.")


# image detection tool
@client.on(events.NewMessage(pattern=r'!img'))
async def img_handler(event):
    if event.sender_id == User_id:
        # Extracting the message content
        message = event.message.message
        # Extracting the image file from the message
        if event.message.reply_to_msg_id:
            # Get the original message that was replied to
            replied_msg = await event.get_reply_message()
            # Check if the replied message contains an image
            if replied_msg.media and hasattr(replied_msg.media, 'photo'):
                # Get the image sender's ID
                img_sender = replied_msg.sender_id
                # Download the image file
                image = await replied_msg.download_media()
                # Extract the query from the message
                query = message.split('!img')[1].strip()
                # Call the img_ai function with the image and query as arguments
                result = ai.image_ai(image, query)
                # Send the result back as a reply to the image sender within the same chat
                await event.reply(result)
                # Remove the downloaded image file
                os.remove(image)
            else:
                # If no image is found in the replied message, send a reply indicating that an image is required
                await event.reply('Please reply to a message containing an image.')
        else:
            # If no message is replied to, send a reply indicating that a message needs to be replied to
            await event.reply('Please reply to a message containing an image.')
    else:
        await event.respond("Sorry, you are not authorized to use this command.")



# just simple spam cmd with 10
@client.on(events.NewMessage(pattern='!spam'))
async def handle_message(event):
    if event.sender_id == User_id: 
        message = event.message.message
        if len(message.split()) > 1:
            response = ' '.join(message.split()[1:])
            for i in range(5):
                await event.respond(response)
        else:
            await event.respond("Please add a message to be spammed.")
    else:
        await event.respond("Sorry, you are not authorized to use this command.")
        
        
# add limited reaction for any massage
@client.on(events.NewMessage(pattern='!react'))
async def handle_reaction(event):
    if event.is_reply:
        try:
            words = event.message.message.split()  # Split into words
            if len(words) >= 2:
                reaction_emoji = words[1]
                # print(reaction_emoji)
            else:
                raise ValueError("Missing emoji in command. Usage: !react <emoji>")

            reply_message = await event.get_reply_message()

            # Get the peer (either a user, chat, or channel)
            peer = await client.get_input_entity(reply_message.sender_id)

            await client(SendReactionRequest(
                peer=peer,
                msg_id=reply_message.id,
                reaction=[types.ReactionEmoji(emoticon=reaction_emoji)]))

            await event.respond(f"Reaction {reaction_emoji} added successfully.")
        except Exception as e:
            await event.respond(f"Error: {str(e)}")
    else:
        await event.respond("Please reply to a message to add a reaction.")


# intro cmd
@client.on(events.NewMessage(pattern='!intro'))
async def intro(event):
    if event.sender_id == User_id:
        user_id = event.sender_id
        message_id = event.message.id
        with open("intro.txt", "rt", encoding="utf-8") as f:
            data = f.read()
            await event.respond(data)
            await asyncio.sleep(2)
            await event.client.delete_messages(event.chat_id, [message_id, event.message.id])
            

# skill cmd
@client.on(events.NewMessage(pattern='!skill'))
async def intro(event):
    if event.sender_id == User_id:
        user_id = event.sender_id
        message_id = event.message.id
        with open("skill.txt", "rt", encoding="utf-8") as f:
            data = f.read()
            await event.respond(data)
            await asyncio.sleep(2)
            await event.client.delete_messages(event.chat_id, [message_id, event.message.id])




async def main():
    # Connect to Telegram
    await client.start(phone_number)
    print("Bot started, listening for messages...")
    # Run the client until Ctrl+C is pressed
    await client.run_until_disconnected()

# Run the main function
if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Stopping the bot...")
        exit()