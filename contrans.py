import numpy as np
import pandas as pd
import os
import requests
import dotenv
import json

class contrans:
    def __init__(self):
        """
        Initializes a contrans object.
        
        Parameters:
        None
        
        Returns:
        None
        """
        self.mypassword = os.getenv("mypassword")
        self.congresskey=os.getenv("congresskey")
        self.newskey=os.getenv("newskey")
        
    def get_votes(self):
        """
        Retrieves 118th congressional voting data from a remote CSV file.
        
        Parameters:
        None
        
        Returns:
        votes (pd.DataFrame): A pandas DataFrame containing the voting data.
        """
        url = 'https://voteview.com/static/data/out/votes/H118_votes.csv'
        votes = pd.read_csv(url)
        return votes
    
        
    def get_ideology(self):
        """
        Retrieves the ideology of members of the 118th congress from a remote CSV file.

        Parameters:
        None

        Returns:
        df (pd.DataFrame): A pandas DataFrame containing the ideology of the members.
        """
        url = 'https://voteview.com/static/data/out/members/H118_members.csv'
        members = pd.read_csv(url)
        return members
    
    def get_useragent(self):
        """
        Retrieves the user agent of the members of the 118th congress from a remote CSV file.

        Parameters:
        None

        Returns:
        df (pd.DataFrame): A pandas DataFrame containing the user agent of the members.
        """
        url = 'https://httpbin.org/user-agent'
        r=requests.get(url)
        useragent = json.loads(r.text)['user-agent']
        return useragent
    

    def make_headers(self, 
                     email='mathaimadelyn@gmail.com'):
        useragent=self.get_useragent()
        headers = {
            'User-Agent': useragent,
            'From': email
        }
        return headers
    
    def get_bioguideIDs(self):
        params = {'api_key': self.congresskey}
        headers=self.make_headers()
        root = 'https://api.congress.gov/v3'
        endpoint = '/member'
        r = requests.get(root+endpoint, 
                         headers=headers, 
                         params=params)
        bio_df = pd.json_normalize(r.json, record_path=['members'])
        bio_df=bio_df[['name','state', 'district', 'bioguideId', 'partyName']]
        return bio_df
    