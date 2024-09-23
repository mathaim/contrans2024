import numpy as np
import pandas as pd
import os

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
        
    def get_votes(self):
        """
        Retrieves congressional voting data from a remote CSV file.
        
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
        Retrieves the ideology of members of the congress from a remote CSV file.

        Parameters:
        None

        Returns:
        df (pd.DataFrame): A pandas DataFrame containing the ideology of the members.
        """
        url = 'https://voteview.com/static/data/out/members/H118_members.csv'
        members = pd.read_csv(url)
        return members
    