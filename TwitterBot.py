from Twitter import Twitter
from LanguageModel import LanguageModel
import pickle


print('Starting Up Twitter Bot Server')
twitter = Twitter()
# The number of words to use for ngram

# try:
    # 3-Gram Langauge Model, only on ISL
    # with open(f'./models/LanguageModel3_ISL.pkl', "rb") as model_pickle:
    #     model = pickle.load(model_pickle)
    
    # 4-Gram Langauge Model, Both ISL, and MIM
with open(f'./models/LanguageModel4_ISLMIM.pkl', "rb") as model_pickle:
    model = pickle.load(model_pickle)
# except:
#     print('Please Unzip: ./models/models.zip into its dir')


# Establishing user stream for my bot
for item in twitter.get_user_stream():
    if 'in_reply_to_user_id_str' in item and item['in_reply_to_user_id_str'] == twitter.user_id_str:
        # Receive data about the sender and the tweet
        sender_tweet_id = item['id'] if 'id' in item else ''
        sender_user_name = item['user']['screen_name'] if 'user' in item and 'screen_name' in item['user'] else ''
        sender_tweet_text = item['text'] if 'text' in item else ''

        # Generate Response
        bot_response = model.generate_response(sender_tweet_text)

        # Retweet
        if bot_response:
            bot_response = f'@{sender_user_name} {bot_response}'
        else:
            bot_response = f'@{sender_user_name} VILLA KOM UPP! Ekki var hægt að nota Tístið þitt.'
        
        twitter.reply_message_to(bot_response, sender_tweet_id)