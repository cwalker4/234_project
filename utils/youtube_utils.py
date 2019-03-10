# adapted from https://github.com/youtube/api-samples/blob/master/python/*

import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


KEY_LOC = os.path.join(os.path.dirname(__file__), '../credentials/api_key.txt')
with open(KEY_LOC, 'r') as f:
    DEVELOPER_KEY = f.read()

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

def search(query, max_results=10):
    """
    Searches YouTube and returns the top result 

    INPUT:
        query: (str) search term
        max_results: (int) maximum number of results to return

    OUTPUT:
        top_result: (dict) top search result ID and title

    """

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
      q=query,
      part='id,snippet',
      maxResults=max_results,
      type='video'
    ).execute()
  
    results = {}
  
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId'].encode('ascii', 'ignore')
        results[video_id] = search_result['snippet']['title'].encode('ascii', 'ignore')

    return results


def get_metadata(video_id):
    """
    Gets the video metadata for the video matching video_id

    INPUT:
        video_id: (str)

    OUTPUT:
        result: (dict) video metadata
    """

    # Call the videos.list method to retrieve results matching the
    # specified video_id
    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, contentDetails, statistics'
        ).execute()

    result = {}

    for video_result in video_response.get('items', []):
        # Get video title, publication date, description, category_id
        snippet = video_result.get('snippet')
        result['title'] = snippet.get('title', -1)
        result['date'] = snippet.get('publishedAt', -1)
        result['description'] = snippet.get('description', -1)
        result['category_id'] = snippet.get('categoryId', -1)
        result['channel'] = snippet.get('channelTitle', -1)

        # Get video caption indicator and duration
        contentDetails = video_result.get('contentDetails')
        result['has_captions'] = contentDetails.get('caption', -1)
        result['duration'] = contentDetails.get('duration', -1)

        # Get like/dislikes, views, n_comments
        statistics = video_result.get('statistics')
        result['likes'] = statistics.get('likeCount', -1)
        result['dislikes'] = statistics.get('dislikeCount', -1)
        result['views'] = statistics.get('viewCount', -1)
        result['n_comments'] = statistics.get('commentCount', -1)

    return result

def get_comments(video_id, max_results=5):
    """
    Gets the top comments for a video_id

    INPUT:
        video_id: (str) 
        max_results: (str) max number of comments to return

    OUTPUT:
        result: (str array) top n comments
    """

    comment_request = youtube.commentThreads().list(
        videoId=video_id,
        maxResults=max_results,
        textFormat='plainText',
        part='snippet',
        order='relevance')

    try:
        comment_response = comment_request.execute()
    except HttpError:
        return -1

    result = []
    for comment_result in comment_response.get('items', []):
        comment = comment_result['snippet']['topLevelComment']
        result.append(comment['snippet']['textOriginal'].encode('ascii', 'ignore'))

    return(result)









