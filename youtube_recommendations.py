# code adapted from Guillaume Chaslot
from __future__ import unicode_literals

import urllib2
import re
import json
import sys
import argparse
import time
import os

from bs4 import BeautifulSoup
import youtube_dl

from utils import youtube_utils


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--query', help='The start search query')
parser.add_argument('--n_roots', default='5', type=int, help='The number of search results to start the exploration')
parser.add_argument('--n_splits', default='3', type=int, help='The branching factor of the exploration tree')
parser.add_argument('--depth', default='5', type=int, help='The depth of the exploration')
parser.add_argument('--loc', help='Location passed to YouTube e.g. US, FR, GB, DE...')
parser.add_argument('--lang', default='en', help='Languaged passed to HTML header, en, fr, en-US, ...')


class YoutubeFollower():
    def __init__(self, n_splits, depth, verbose=False, loc=None, lang=None):
        self._verbose = verbose

        self._video_info = {}
        self._search_info = {}
        self._loc = loc
        self._lang = lang

        self._n_splits = n_splits
        self._depth = depth


    def save_results(self, out_dir):
        """
        Dumps video_info and search_info as jsons

        INPUT:
            out_dir: (str) directory to save the files

        """
        params_dict = {'n_splits': self._n_splits,
                       'depth': self._depth}

        os.makedirs(out_dir)

        with open(os.path.join(out_dir, 'video_info.json'), 'w') as f:
            json.dump(yf._video_info, f)

        with open(os.path.join(out_dir, 'search_info.json'), 'w') as f:
            json.dump(yf._search_info, f)

        with open(os.path.join(out_dir, 'params.json'), 'w') as f:
            json.dump(params_dict, f)


    def get_subtitles(self, video_id):
        """
        Saves the subtitle track for video_id

        INPUT:
            video_id: (str)
        """

        url = "https://youtube.com/watch?v={}".format(video_id)

        yt_opts = {"skip_download": True,
                   "writesubtitles": True,
                   "subtitlelangs": self._lang,
                   "outtmpl": "results/captions/%(id)s.vtt",
                   "no_warnings": True,
                   "quiet": True}

        with youtube_dl.YoutubeDL(yt_opts) as yt:
            yt.download([url])


    def populate_info(self, video_id):
        """
        Fills the video info dictionary with video data

        INPUT:
            video_id: (str)
        """

        # Download the subtitles if available
        self.get_subtitles(video_id)

        # Get the metadata and comments
        metadata = youtube_utils.get_metadata(video_id)
        comments = youtube_utils.get_comments(video_id, max_results=10)
        self._video_info[video_id] = {'views': metadata['views'],
                                     'likes': metadata['likes'],
                                     'dislikes': metadata['dislikes'],
                                     'description': metadata['description'],
                                     'category': metadata['category_id'],
                                     'postdate': metadata['date'],
                                     'n_comments': metadata['n_comments'],
                                     'channel': metadata['channel'],
                                     'title': metadata['title'],
                                     'comments': comments,
                                     'id': video_id}

        video = self._video_info[video_id]
        print("\nLogging info for {}: {}".format(video_id, video['title']))


    def get_recommendations(self, video_id, n_recs, depth):
        """
        Scrapes the recommendations corresponding to video_id

        INPUT:
            video_id: (str) 
            n_recs: (int) number of recommendations to get
            depth: (int) depth of search
            
        OUTPUT:
            recs: (list) list of recommended video_ids
        """

        # If we're a leaf node, don't get recommendations
        if depth == self._depth:
            self._search_info[video_id] = {'recommendations': [],
                                           'depth': depth}
            return []

        # Get recommendations via BeautifulSoup
        url = "https://youtube.com/watch?v={}".format(video_id)

        while True:
            try:
                html = urllib2.urlopen(url)
                break
            except urllib2.URLError:
                time.sleep(1)
        soup = BeautifulSoup(html, "lxml")

        recs = []
        upnext = True
        for video_list in soup.findAll('ul', {'class': 'video-list'}):
            if upnext:
                try:
                    rec_id = video_list.contents[1].contents[1].contents[1]['href'].replace('/watch?v=', '')
                    recs.append(rec_id)
                except IndexError:
                    print ('WARNING Could not get a up next recommendation because of malformed content')
                    pass
                upnext = False
            else:
                for i in range(1, n_recs):
                    try:
                        rec_id = video_list.contents[i].contents[1].contents[1]['href'].replace('/watch?v=', '')
                        recs.append(rec_id)
                    except IndexError:
                        print('There are not enough recommendations')
                    except AttributeError:
                        print('WARNING Malformed content, could not get recommendation')

        # Comment me in for DFS tree
        #self._search_info[video_id] = {'recommendations': recs[:n_recs],
        #                               'depth': self._depth - depth}

        self._search_info[video_id] = {'recommendations': recs[:n_recs],
                                       'depth': depth}

        print("Recommendations for video {}: {}".format(video_id, recs))

        return recs


    def get_recommendation_tree(self, seed, n_splits):
        """
        Builds the recommendation tree via BFS. Calls functions to 
        populate video info and search info.

        INPUT:
            seed: (str) video_id of tree root
            n_splits: (int) number of splits at each vertex
            depth: (int) depth of tree
        """
        queue = []
        inactive_queue = []
        queue.append(seed)

        depth = 0
        while depth <= self._depth:
            if not queue and not inactive_queue:
                return
            if not queue:
                queue = inactive_queue
                inactive_queue = []
                depth += 1
            current_video = queue.pop(0)
            self.populate_info(current_video)
            recs = self.get_recommendations(current_video, n_splits, depth)
            for video_id in recs:
                if video_id in self._video_info:
                    print("Video {} has already been visited".format(video_id))
                    continue
                inactive_queue.append(video_id)


    def get_recommendation_tree_dfs(self, seed, n_splits, depth):
        """
        Recursively builds the recommendation tree via DFS. Calls functions to 
        populate video info and search info. Default format of code will not work
        out-of-the box; see inline comments.

        INPUT:
            seed: (str) video_id of tree root
            n_splits: (int) number of splits at each vertex
            depth: (int) depth of tree
        """
        if depth == 0:
            return
        current_video = seed

        for video in self.get_recommendations(current_video, n_splits, depth):
            if video in self._video_info:
                print("Video {} has already been visited".format(video))
                continue
            self.populate_info(video)
            self.get_recommendation_tree(video, n_splits, depth - 1)


    def search(self, root_id):
        self.get_recommendation_tree(seed=root_id,
                                     n_splits=self._n_splits)

        # Comment me in for DFS tree
        #self.get_recommendation_tree(seed=root_id,
        #                             n_splits=self._n_splits,
        #                             depth=self._depth)



if __name__ == "__main__":
    args = parser.parse_args()

    root_videos = youtube_utils.search(args.query, max_results=args.n_roots)
    for video_id in root_videos:
        print('Starting search with query {} and root video {}'.format(args.query, video_id))
        out_dir = 'results/{}_{}'.format(args.query, video_id)

        if os.path.exists(out_dir):
            print('Search already done; skipping\n\n\n')
            continue
        
        yf = YoutubeFollower(
            n_splits=args.n_splits,
            depth=args.depth,
            verbose=True, 
            loc=args.loc, 
            lang=args.lang)

        yf.search(root_id=video_id)

        yf.save_results(out_dir)
        print("\n\n\n")



