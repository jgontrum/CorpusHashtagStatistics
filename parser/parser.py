import re


class FileParser(object):

    def __init__(self, filename):
        super(FileParser, self).__init__()
        self.filename = filename
        self.hashtag_counter = {}
        self.number_of_hashtags_in_tweet = {}
        self.number_of_tweets = 0
        self.number_of_tweets_with_hashtag = 0
        self.number_of_hashtags = 0
        self.abs_number_of_hashtags = 0

        self.hashtag_histogram = ""
        self.most_common_hashtag = None

        self.parse(filename)
        self.make_statistics()

    def extract_hashtags(self, text):
        return re.findall(r"#[\w\d]+", text, re.IGNORECASE)

    def parse(self, filename):
        raise Exception("Not implemented.")

    def process_text(self, text):
        hashtags = self.extract_hashtags(text)

        # Count how often a hashtag appears
        for hashtag in hashtags:
            hashtag = hashtag.strip()
            hashtag = hashtag.lower()
            self.hashtag_counter.setdefault(hashtag, 0)
            self.hashtag_counter[hashtag] += 1

        # Count number of hashtags in tweet
        self.number_of_hashtags_in_tweet.setdefault(len(hashtags), 0)
        self.number_of_hashtags_in_tweet[len(hashtags)] += 1

    def make_statistics(self):
        self.number_of_tweets = sum(self.number_of_hashtags_in_tweet.values())

        self.number_of_tweets_with_hashtag = sum(
            [v for k, v in self.number_of_hashtags_in_tweet.items()
             if k > 0])

        self.number_of_hashtags = len(self.hashtag_counter.keys())

        self.abs_number_of_hashtags = sum(self.hashtag_counter.values())

        tags = sorted(self.hashtag_counter.items(),
                      key=lambda x: x[1],
                      reverse=True)

        self.most_common_hashtag = tags[0] if tags else ("NONE", 0)

        self.hashtag_histogram = [
            (k, self.number_of_hashtags_in_tweet.get(k, 0))
            for k in range(1, max(self.number_of_hashtags_in_tweet.keys()) + 1)
        ]

    def get_data_as_dict(self):
        ret = {
            "Number Of Tweets": self.number_of_tweets,
            "Number Of Hashtags": self.number_of_hashtags,
            "Absolute Number Of Hashtags": self.abs_number_of_hashtags,
            "Tweets with Hashtag": self.number_of_tweets_with_hashtag,
            "Most Common Hashtag": self.most_common_hashtag[0],
            "Most Common Hashtag Count": self.most_common_hashtag[1]
        }

        ret.update({
            "#_{}".format(k): self.number_of_hashtags_in_tweet.get(k, 0)
            for k in range(1, max(self.number_of_hashtags_in_tweet.keys()) + 1)
        })

        return ret

    def __repr__(self):
        t = str()
        t += "Tweets:\t\t\t{tweets}\nTweets with Hashtag:\t{tweets_w_hashtag}\n"
        t += "Absolute Number of Hashtags:\t{abs_hashtags}\n"
        t += "Number of Hashtags:\t{hashtags}\n"
        t += "Most common Hashtag:\t{common_hashtag[0]} [{common_hashtag[1]}x]\n"
        t += "Hashtag Histogram:\t{hashtag_histogram}"
        return t.format(tweets=self.number_of_tweets,
                        common_hashtag=self.most_common_hashtag,
                        tweets_w_hashtag=self.number_of_tweets_with_hashtag,
                        hashtags=self.number_of_hashtags,
                        abs_hashtags=self.abs_number_of_hashtags,
                        hashtag_histogram=self.hashtag_histogram)


class FileParserCSV(FileParser):

    def parse(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if not line:
                    continue
                try:
                    self.process_text("".join(line.split(',')[2:]).strip('"'))
                except Exception:
                    print("Could not read line:'{}'".format(line.__repr__()))


class FileParserText(FileParser):

    def parse(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if not line or not line.strip():
                    continue
                try:
                    self.process_text(line.strip())
                except Exception as e:
                    pass


class FileParserPipe(FileParser):

    def parse(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if not line:
                    continue
                try:
                    self.process_text("".join(line.split('|')[6:]).strip())
                except Exception:
                    print("Could not read line:'{}'".format(line.__repr__()))
