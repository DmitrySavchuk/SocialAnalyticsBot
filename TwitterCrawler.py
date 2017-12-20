import tweepy


class TwitterCrawler:
    def __init__(self):
        self.consumer_key = "JaLm8Ft9Wft5b02m1bAmHsa0S"
        self.consumer_secret = "PVHzVhWlCEwVakVAwUbcGXNTYJWHHYKkAf1BYSiMxMMOD7FyvY"
        self.access_key = "527809087-BKtvl8pdHUOKFP4QD3UoqW7JWAjWLKqChMXl3a2h"
        self.access_secret = "VBZqCinjj9Yafj36bn9QiydyToy4ScRBhLd0sYIDEk1hL"
        self.api = tweepy.API(self.auth)

    @property
    def auth(self):
        """Установка соединения."""
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        return auth

    def tweet_search(self, query, loc=None):
        """Поиск твитов."""
        text = ''
        if loc:
            geo = self.__get_loc(loc)
            results = self.api.search(q=query, count=100, lang='en', geocode=geo)
        else:
            results = self.api.search(q=query, count=100, lang='en')
        for tweet in results:
            text += tweet.text
        return text

    def __get_loc(self, loc):
        """Определение geocode"""
        geo = ''
        k = []
        num = True
        results = self.api.geo_search(query=loc, granularity="country")
        for tweet in results:
            while num:
                for tweet_loc in tweet.centroid:
                    k.append(tweet_loc)
                    num = False
        k.reverse()
        for item in k:
            geo += str(item) + ','
        geo += '200km'
        return geo
