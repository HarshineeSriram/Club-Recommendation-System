# -*- coding: utf-8 -*-
import re
import json
from collections.abc import Iterable
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


CLEAN_LINK = re.compile('(?<=^\/)\/+|\/+$')
CLEAN_WORD = re.compile('[\[\],().:;"\/\'?*%!*+=@$;#%{}`~\r\n\t]')
LONG_DASH = re.compile('(\&#8212;)')
MIN_TAG_LENGTH = 2
SMART_QUOTES_D = re.compile('(\xe2\x80\x9c)|(\xe2\x80\x9d)|(\&#8220;)|(\&#8221;)')
SMART_QUOTES_S = re.compile('(\xe2\x80\x98)|(\xe2\x80\x99)|(\&#8216;)|(\&#8217;)')
STOP_WORDS = ['DT', 'IN', 'TO', 'VBD', 'VBD', 'VBG', 'VBN', 'VBZ', 'MD', 'RB',
              'CC', 'WDT', 'PRO', 'PRP', 'PRP$']


class generate_intelligent_tags:
    lemma = WordNetLemmatizer()

    def __init__(self):
        self.css = ''
        self.link = ''
        self.text = ''

    def create_tokens(self):
        """Tag words from the string."""
        return nltk.pos_tag(nltk.word_tokenize(self.clean_text()))

    def clean_words(self, word, strict):
        lemmatized = self.lemma.lemmatize(self.clean_text(word))
        if strict:
            return lemmatized
        else:
            return quote(self.clean_text(word))

    def clean_text(self, word=''):
        if len(word) > MIN_TAG_LENGTH:
            return CLEAN_WORD.sub('', self.replace_special_chars(word.lower()))
        else:
            return CLEAN_WORD.sub('', self.replace_special_chars(self.text))

    def replace_special_chars(self, text):
        return SMART_QUOTES_S.sub('\'', SMART_QUOTES_D.sub('"', LONG_DASH.sub('-',text)))

    def generate(self, strict=True):
        """Return the HTML version of tags for the string."""
        tag_words = []
        for (word, word_type) in self.create_tokens():
            tag_word = self.clean_words(word, strict)
            if len(tag_word) > MIN_TAG_LENGTH and word_type not in STOP_WORDS:
                tag_words.append('<a href="%s/%s" class="%s">%s</a> ' % (CLEAN_LINK.sub('', self.link),
                                                                         quote(tag_word),
                                                                         CLEAN_WORD.sub('', self.css),
                                                                         self.replace_special_chars(word)))
            else:
                tag_words.append(word + ' ')
        return ''.join(tag_words)

    def tag_list(self, strict=True):
        """Return the tags from string as a list. If strict is set
        to True, then only return the stemmed version. Otherwise, return the
        full string - therefore, `cat` will be considered different from `cats`.
        """
        tag_words = []
        for (word, word_type) in self.create_tokens():
            tag_word = self.clean_words(word, strict)
            if len(tag_word) > MIN_TAG_LENGTH and word_type not in STOP_WORDS:
                tag_words.append(tag_word)
        return tag_words

class generate_club_tags:
    def __init__(self) -> None:
        #print("\n 1) Loading initial parameters. . .")
        initial_parameters = open(r'initial_parameters.json')
        initial_parameters = json.load(initial_parameters)

        self.number_of_students = initial_parameters['number_of_students']
        f_clubs = open(initial_parameters['paths']['path_to_all_clubs'],)
        f_events = open(initial_parameters['paths']['path_to_all_events'],)

        self.data_clubs = json.load(f_clubs)
        self.data_events = json.load(f_events)
        self.faculties = initial_parameters['faculties']

        self.number_of_clubs = len(self.data_clubs)
        self.number_of_events = len(self.data_events)

        self.club_titles = [self.data_clubs[i]['title'] for i in range(
            self.number_of_clubs)]
        self.event_ids = [self.data_events[i]['eventId'] for i in range(
            self.number_of_events)]

    def remove_long_tags(self, club_index, data_clubs):
        for tag in self.data_clubs[club_index]['categories']:
            if len(tag)>10:
                self.data_clubs[club_index]['categories'].remove(tag)

    def generate_better_tags(self):
        print("\n 2) Processing club titles and descriptions. . .")
        for i in range(self.number_of_clubs):
            club_index = i
            t = generate_intelligent_tags() # For processing club titles and descriptions
            if('description' in self.data_clubs[i]):
                t.text = self.data_clubs[i]['title'] + " " + self.data_clubs[i]['description']
                if self.data_clubs[i]['categories'] == None:
                    self.data_clubs[i]['categories'] = list(set(t.tag_list()))
                    self.remove_long_tags(club_index, self.data_clubs)
                else:
                    self.data_clubs[i]['categories'] = list(set(t.tag_list()))
                    self.remove_long_tags(club_index, self.data_clubs)
            else:
                t.text = self.data_clubs[i]['title']
                this_tag_list = set(t.tag_list())
                self.data_clubs[i]['categories'] = list(set(t.tag_list()))
                self.remove_long_tags(club_index, self.data_clubs)

    def flatten_multid_list(self, l:list):
        for this_l in self.l:
            if isinstance(this_l, Iterable) and not isinstance(this_l, (str, bytes)):
                yield from self.flatten_multid_list(this_l)
            else:
                yield this_l