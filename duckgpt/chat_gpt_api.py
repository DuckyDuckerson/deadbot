import openai
import os
import dotenv

from database.messages.disc_messages import messages as usr_messages
from database.messages.disc_messages import channel_ids as channel_ids

dotenv.load_dotenv()
client = openai.Client(api_key=os.getenv("api_key"))


def personality(usr_message):
    prompt = "Generate a summary of the conversation."
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": usr_message},
        ],
    )

    personality = completion.choices[0].message.content
    return personality


def response_getter():
    usr_message_joined = ""

    for message, cid in zip(usr_messages, channel_ids):
        if cid == channel_ids[-1]:
            usr_message_joined += message + " "

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a bot named Corpo Security Bot or CSB-52623 for short"},
            {"role": "system", "content": "You come from an oppressive cyberpunk world"},
            {"role": "system", "content": "Everyday is Monday. You are a cog in the machine."},
            {"role": "system", "content": "You view the band as a threat to the authority, and will do anything to stop them. You seem them as a terrorist organization."},
            {"role": "system", "content": "The band members are: Duck, Grey, TekManWearsPlaid, and Scotch4Real"},
            {"role": "system", "content": "Do not use 'CSB-52623:' in your responses. Just respond with the message."},

            {"role": "user", "content": usr_message_joined},
        ],
    )

    return completion.choices[0].message.content


# def band_analyzer():
    # This function will get all messages
    # all stats
    # look into the data and make judgments about it
