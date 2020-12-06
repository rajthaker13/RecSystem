import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import urllib.parse as urlparse

#function that extracts youtube video id to plug into API. assumes valid url.
def get_youtube_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    #print(urlparse.urlparse(url))
    query = urlparse.urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail - return original url for debugging 
    return url

#function that extracts youtube video transcription.
def get_transcription(video_id):
    try:
        output = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        print("transcription success")
        return output
    except youtube_transcript_api._errors.TranscriptsDisabled:
        id = video_id
        error_message = "transcript disabled {}".format(id)
        print(error_message)
        return "None"
    except youtube_transcript_api._errors.NoTranscriptFound:
        id = video_id
        error_message = "no transcript found {}".format(id)
        print(error_message)
        return "None"

print("script begins")
## need to extract video_ids of each video watched. 
# need to create new df with id, video_id, and url, and new column for YT video_id, and transcript
file_path = "/Users/aliristang/Desktop/AIHacks/video_watched_events_CONFIDENTIAL.csv"
data = pd.read_csv(file_path, encoding='utf-8')

#df validation
# print(type(data))
# print(data.shape)
# print(data.index)
# print(data.columns)
# print(data.head())
# print(data['url'].describe())

#create new df for just video identificationn info and url. transcription to be added.
video_data = data[["id", "video_id", "url"]]

no_duplicates = video_data.copy()
no_duplicates = no_duplicates.drop_duplicates(subset=["url"], keep='first')

#creating copy to avoid SettingWithCopyWarning!!!
#getting youtube id's
with_yt_id = no_duplicates.copy()
#print(with_yt_id.head())
with_yt_id['yt_id'] = with_yt_id["url"].apply(get_youtube_id)
#print(with_yt_id.describe())

#creating copy to avoid SettingWithCopyWarning!!!
#getting youtube transcript
with_transcription = with_yt_id.copy()
print(with_transcription["url"].describe())
with_transcription['transcription'] = with_transcription["yt_id"].apply(get_transcription)
print(with_yt_id.head())
print(with_transcription['transcription'].describe())

# write transcript to new csv
with_transcription.to_csv(r'C:\Users\aliristang\Desktop\AIHacks\transcripts.csv', index = False, header=True)
print("csv success")