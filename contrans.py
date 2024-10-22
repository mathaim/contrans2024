import numpy as np
import pandas as pd
import os
import requests
import dotenv
import json
from bs4 import BeautifulSoup

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
        self.us_state_to_abbrev = {
                        "Alabama": "AL","Alaska": "AK","Arizona": "AZ","Arkansas": "AR",
                        "California": "CA","Colorado": "CO","Connecticut": "CT","Delaware": "DE",
                        "Florida": "FL","Georgia": "GA","Hawaii": "HI",
                        "Idaho": "ID","Illinois": "IL","Indiana": "IN","Iowa": "IA",
                        "Kansas": "KS","Kentucky": "KY","Louisiana": "LA",
                        "Maine": "ME","Maryland": "MD","Massachusetts": "MA",
                        "Michigan": "MI","Minnesota": "MN","Mississippi": "MS",
                        "Missouri": "MO","Montana": "MT","Nebraska": "NE",
                        "Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ",
                        "New Mexico": "NM","New York": "NY","North Carolina": "NC",
                        "North Dakota": "ND","Ohio": "OH","Oklahoma": "OK",
                        "Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI",
                        "South Carolina": "SC","South Dakota": "SD","Tennessee": "TN",
                        "Texas": "TX","Utah": "UT","Vermont": "VT",
                        "Virginia": "VA","Washington": "WA","West Virginia": "WV",
                        "Wisconsin": "WI","Wyoming": "WY","District of Columbia": "DC",
                        "American Samoa": "AS","Guam": "GU","Northern Mariana Islands": "MP",
                        "Puerto Rico": "PR","United States Minor Outlying Islands": "UM",
                        "Virgin Islands": "VI"
                        }


        
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
    

    def get_bioguideIDs(self, congress=118):
        params = {'api_key': self.congresskey,
                          'limit': 1} 
        headers = self.make_headers()
        root = 'https://api.congress.gov/v3'
        endpoint = f'/member/congress/{congress}'
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
        bills_list = []
        bio_df = pd.DataFrame()
        while j < totalrecords:
            params['offset'] = j
            r = requests.get(root + endpoint,
                                         params=params,
                                         headers=headers)
            records = r.json()['sponsoredLegislation']
            bills_list= bills_list + records
            j = j + 250

        return bills_list
    def make_cand_table(self):
                members = self.get_bioguideIDs()
                replace_map = {'Republican': 'R','Democratic': 'D','Independent': 'I'}
                members['partyletter'] = members['partyName'].replace(replace_map)
                members['state'] = members['state'].replace(self.us_state_to_abbrev)
                members['district'] = members['district'].fillna(0)
                members['district'] = members['district'].astype('int').astype('str')
                members['district'] = ['0' + x if len(x) == 1 else x for x in members['district']]
                members['district'] = [x.replace('00', 'S') for x in members['district']]
                members['DistIDRunFor'] = members['state']+members['district']
                members['lastname']= [x.split(',')[0] for x in members['name']]
                members['firstname']= [x.split(',')[1] for x in members['name']]
                members['name2'] = [ y.strip() + ' (' + z.strip() + ')' 
                                for y, z in 
                                zip(members['lastname'], members['partyletter'])]
                
                cands = pd.read_csv('data/CampaignFin22/cands22.txt', quotechar="|", header=None)
                cands.columns = ['Cycle', 'FECCandID', 'CID','FirstLastP',
                                'Party','DistIDRunFor','DistIDCurr',
                                'CurrCand','CycleCand','CRPICO','RecipCode','NoPacs']
                cands['DistIDRunFor'] = [x.replace('S0', 'S') for x in cands['DistIDRunFor']]
                cands['DistIDRunFor'] = [x.replace('S1', 'S') for x in cands['DistIDRunFor']]
                cands['DistIDRunFor'] = [x.replace('S2', 'S') for x in cands['DistIDRunFor']]
                cands['name2'] = [' '.join(x.split(' ')[-2:]) for x in cands['FirstLastP']]
                cands = cands[['CID', 'name2', 'DistIDRunFor']].drop_duplicates(subset=['name2', 'DistIDRunFor'])
                crosswalk = pd.merge(members, cands, 
                     left_on=['name2', 'DistIDRunFor'],
                     right_on=['name2', 'DistIDRunFor'],
                     how = 'inner')
                return crosswalk
    
    def get_billdata(self, billurl):
        r = requests.get(billurl,
                    params = {'api_key':self.congresskey})
        bill_json = json.loads(r.text)
        texturl = bill_json['bill']['textVersions']['url']
        r = requests.get(texturl,
                        params= {'api_key':self.congresskey})
        toscrape = json.loads(r.text)['textVersions'][0]['formats'][0]['url']
        r = requests.get(toscrape)
        mysoup = BeautifulSoup(r.text, 'html.parser') #equivalent of json.loads, allows you to search through a string
        billtext = mysoup.text
        bill_json['bill_text'] = billtext

    def terms_df(self, members):
                termsDF = pd.DataFrame()
                for index, row in members.iterrows():
                        bioguide_id = row['bioguideId']
                        terms = row['terms.item']
                        df = pd.DataFrame.from_records(terms)
                        df['bioguideId'] = bioguide_id
                        termsDF = pd.concat([termsDF, df])
                members = members.drop('terms.item', axis=1)
                return termsDF, members