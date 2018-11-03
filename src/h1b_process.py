import pandas as pd

class h1b_process():
    def __init__(self, df, state_output_filename, occup_output_filename):
        self.df = df
        self.state_output_filename = state_output_filename
        self.occup_output_filename = occup_output_filename
        
    def __get_certified_cases_df(self):
        if 'STATUS' in self.df.columns:
            case_status_column = 'STATUS'
        elif 'CASE_STATUS' in self.df.columns:
            case_status_column = 'CASE_STATUS' 
        return self.df[self.df[case_status_column] == 'CERTIFIED']

    def top_occupation(self):
        ## define a dataframe to store processed data. Columns name are same as specified in README file
        ## # TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        soc_name_list_df = pd.DataFrame(columns = ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']) 
        
        ## csv data files have different column names
        ## Look for right column name in the data frame 
        ####  SOC_CNAME column and then for LCA CASE SOC NAME column 
    
        certified_occupations_df = self.__get_certified_cases_df() 
        
        if 'LCA_CASE_SOC_NAME' in certified_occupations_df.columns:
            work_loc_soc_name = 'LCA_CASE_SOC_NAME'
        elif 'SOC_NAME'  in certified_occupations_df.columns:
            work_loc_soc_name =   'SOC_NAME'
        
        # calculate the count of certified applications for each occupation, percentage

        loc = 0 
        for occupation in certified_occupations_df[work_loc_soc_name].unique():
            case_count = certified_occupations_df[certified_occupations_df[work_loc_soc_name] == occupation][work_loc_soc_name].count()
            percent = (case_count/certified_occupations_df.shape[0]) * 100.0
            soc_name_list_df.loc[loc] = [occupation, case_count, str(percent)+'%']
            loc = loc + 1
        top_10_occupations_df = soc_name_list_df.sort_values(by=['NUMBER_CERTIFIED_APPLICATIONS', 'TOP_OCCUPATIONS'], ascending=[False, True])[:10]

        # store the result in the output file specified as the input parameter above
        try:
            top_10_occupations_df.to_csv(self.occup_output_filename, sep = ';', index=False)
            if __debug__:
                print("*** Successfully Written data to : " + self.occup_output_filename)
        except IOException:
            print("ERROR: Could not write to file " + self.occup_output_filename)

        if __debug__:
            print(top_10_occupations_df)
            print("Occupations List : ", certified_occupations_df[work_loc_soc_name].unique()[:10])
        
        # mark the object for deletion to conserver memory        
        del certified_occupations_df    

    def top_state(self):
        ## define a dataframe to store processed data. Columns name are same as specified in README file
        states_list_df = pd.DataFrame(columns = ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']) # TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        
        ## csv data files have different column names
        ## Look for right column name in the data frame
        ####  WORKSITE_STATE column and for wLCA_CASE_WORKLOC1_STATE column   

        certified_state_df = self.__get_certified_cases_df()
        
        if 'LCA_CASE_WORKLOC1_STATE' in certified_state_df.columns:
            work_loc_state_column = 'LCA_CASE_WORKLOC1_STATE'
        elif 'WORKSITE_STATE'  in certified_state_df.columns:
            work_loc_state_column =   'WORKSITE_STATE'
        
        # calculate the count of certified applications for each state, percentage

        loc = 0 
        for state in certified_state_df[work_loc_state_column].unique():
            case_count = certified_state_df[certified_state_df[work_loc_state_column] == state][work_loc_state_column].count()
            percent = (case_count/certified_state_df.shape[0]) * 100.0
            states_list_df.loc[loc] = [state, case_count, str(percent)+'%']
            loc = loc + 1
        top_10_states_df = states_list_df.sort_values(by=['NUMBER_CERTIFIED_APPLICATIONS', 'TOP_STATES'], ascending=[False, True])[:10] 

        # store the result in the output file specified as the input parameter above

        try:
            top_10_states_df.to_csv(self.state_output_filename, sep = ';', index=False)
            if __debug__:
                print("*** Successfully Written data to : " + self.state_output_filename)
        except IOException:
            print("ERROR: Could not write to file " + self.state_output_filename)

        if __debug__:
            print(top_10_states_df)
            print("State List : ", certified_state_df[work_loc_state_column].unique()[:10])

        # mark the object for deletion to conserver memory 
        del certified_state_df     