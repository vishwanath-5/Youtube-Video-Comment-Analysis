from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num_messages, len(words), len(links), df['likes'].sum(), df['replies'].sum()

def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'user':'name', 'count': 'percentage'})
    return x, df

def create_wordcolud(selected_user, df):
    if selected_user!='Overall':
        df = df[df['user']==selected_user]
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df['message']=df['message'].apply(remove_stopwords)
    df_wc = wc.generate((df['message'].str.cat(sep=' ')))
    return df_wc

def most_common_words(selected_user, df):
    if(selected_user!='Overall'):
        df=df[df['user']==selected_user]
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def yearly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    yearly_timeline = df.groupby('year').count()['message'].reset_index()
    return yearly_timeline

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    user_heatmap = df.pivot_table(index = 'year', columns='period', values='message', aggfunc='count')
    return user_heatmap