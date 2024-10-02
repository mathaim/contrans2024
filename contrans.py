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
        params = {'api_key': self.congresskey,
                          'limit': 1} 
        headers = self.make_headers()
        root = 'https://api.congress.gov/v3'
        endpoint = '/member'
        r = requests.get(root + endpoint,
                                 params=params,
                                 headers=headers)
        totalrecords = r.json()['pagination']['count']
                
        params['limit'] = 250
        j = 0
        bio_df = pd.DataFrame()
        while j < totalrecords:
            params['offset'] = j
            r = requests.get(root + endpoint,
                                         params=params,
                                         headers=headers)
            records = pd.json_normalize(r.json()['members'])
            bio_df = pd.concat([bio_df, records])
            j = j + 250

        #bio_df = bio_df[['name', 'state', 'district', 'partyName', 'bioguideId']]
        return bio_df
     
    
    def get_bioguide(self, name, state=None, district=None):
        """
        Retrieves the bioguide ID of a member of Congress based on their name, state, and district.

        Parameters:
            name (str): The name of the member of Congress.
            state (str, optional): The state of the member of Congress. Defaults to None.
            district (str, optional): The district of the member of Congress. Defaults to None.

        Returns:
            str: The bioguide ID of the member of Congress.
        """
        members = self.get_bioguideIDs() # replace with a SQL query once we have it as a SQL table

        members['name'] = members['name'].str.lower().str.strip()
        name = name.lower().strip()

        tokeep = [name in x for x in members['name']] #returning only the ones that match our search
        members = members[tokeep]

        if state is not None:
            members = members.query('state == @state')
        if district:
            members = members.query('district == @district') 
        
        return members.reset_index(drop=True)
    
    def get_sponsoredlegislation(self, bioguideid):
        params = {'api_key': self.congresskey,
                          'limit': 1} 
        
        headers = self.make_headers()
        root = 'https://api.congress.gov/v3'
        endpoint = f'/member/{bioguideid}/sponsored-legislation'
        
        r = requests.get(root + endpoint,
                                 params=params,
                                 headers=headers)
        totalrecords = r.json()['pagination']['count']
                
        params['limit'] = 250
        j = 0
        bio_df = pd.DataFrame()
        while j < totalrecords:
            params['offset'] = j
            r = requests.get(root + endpoint,
                                         params=params,
                                         headers=headers)
            records = r.json()['sponsoredLegislation']
            bills_dict = bills_dict.update(records)
            j = j + 250

        return bills_dict
    
