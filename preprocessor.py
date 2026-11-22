import re
from pytubefix import YouTube
import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT, SORT_BY_POPULAR
import streamlit as st
def preprocess_video(video_url):
    yt = YouTube(video_url)
    data = {
        'title': yt.title,
        'likes': yt.likes,
        'upload_date': yt.publish_date,
        'views': yt.views,
        'duration': yt.length
    }
    data['duration'] = str((yt.length//60)//60)+':'+str((yt.length//60)%60)+':'+ str(yt.length%60)
    video_df = pd.DataFrame([data])
    return video_df
@st.cache_data(show_spinner=False)
def preprocess_comments(video_url):
    downloader = YoutubeCommentDownloader()
    comments_generator = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)
    comments = list(comments_generator)
    data_df = pd.DataFrame(comments)
    df = pd.DataFrame()
    df['user'] = data_df['author']
    df['message'] = data_df['text']
    dates = pd.to_datetime([comment.get('time_parsed') for comment in comments], unit='s', errors='coerce')
    df['date'] = dates
    df['year'] = df['date'].dt.year
    period = []
    for year in df['year']:
        period.append(str(year)+'-'+str(year+1))
    df['period'] = period
    def parse_count(value):
        if pd.isna(value):
            return 0
        value = str(value).strip().lower().replace(',', '')
        match = re.search(r"(\d+(?:\.\d+)?)\s*([kmb]?)", value)
        if not match:
            return 0
        number = float(match.group(1))
        suffix = match.group(2)
        multiplier = {'': 1, 'k':1000, 'm': 1000000, 'b': 1000000000}
        return int(number * multiplier[suffix])
    df['likes'] = data_df['votes'].apply(parse_count)
    df['replies'] = data_df['replies'].apply(parse_count)
    df['photo'] = data_df['photo']
    return df