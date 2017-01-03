from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
import csv
import os.path


'''
See the HipChat api documentation for how to get a user access token.
https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens
'''
train = False
if not (os.path.isfile("./database.json")):
    train = True
    errors = 0

# petbot token f25343ef4555ff7c40e02dc231641e266d1d06b0
chatbot = ChatBot(
    "PetBot",
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    #_host="https://archbang.hipchat.com",
    gitter_room="autio/PetBot2000",
    gitter_api_token="f25343ef4555ff7c40e02dc231641e266d1d06b0",
    gitter_only_respond_to_mentions=False,
    input_adapter="chatterbot.input.Gitter", #TerminalAdapter",
    output_adapter="chatterbot.output.Gitter",
    database="./database.json"
)

if train:
    # Does the training database exist already? If not, train
    # Import training file as a list
    with open('PetTraining.csv', 'r') as f:
        reader = csv.reader(f)
        training_conversations = list(reader)
    f.close()
    # gitter api token 291b8aa0b216cbf5d6429b215f979ada5e0a4ba9

    conversation = [
        "Hello",
        "Hi there!",
        "How are you doing?",
        "I'm doing great.",
        "What's up?",
        "Things are swell.",
        "That is good to hear",
        "Thank you.",
        "You're welcome."
    ]

    chatbot.set_trainer(ListTrainer)
    chatbot.train(conversation)
    for item in training_conversations:
        try:
            chatbot.train(item)
        except:
            errors += 1
    chatbot.set_trainer(ChatterBotCorpusTrainer)
    chatbot.train("chatterbot.corpus.english")



while True:
    try:
        bot_input = chatbot.get_response(None)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break

