
import os
import sys

class h1b_process_no_pandas():

    def __init__(self, h1b_data, state_output_filename, occup_output_filename):
        self.h1b_data = h1b_data
        self.state_output_filename = state_output_filename
        self.occup_output_filename = occup_output_filename
        self.state_idx = 0
        self.occup_idx = 0
        
    def get_certified_cases_count(self):
        count = 0
        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                count = count + 1
        if __debug__:
            print("Certified Case count : ", count)    
        return count   

    def __find_col_idx_state(self):
        if 'WORKSITE_STATE' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('WORKSITE_STATE')  
        elif 'LCA_CASE_WORKLOC1_STATE' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('LCA_CASE_WORKLOC1_STATE') 
        if __debug__:
            print("Column idx : ", idx, self.h1b_data[0][idx]) 
        return idx 


    def __get_states_list(self):
        states_list = []
        self.state_idx = self.__find_col_idx_state()
        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                states_list.append(self.h1b_data[i][self.state_idx])
        if __debug__:
            print("total states : ", len(states_list))
        return states_list

    def find_top_state(self):
        top_10_keystore = {}
        states_list = self.__get_states_list()
        for state in states_list:
            top_10_keystore[state] = 0

        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                idx = states_list.index(self.h1b_data[i][self.state_idx])
                top_10_keystore[states_list[idx]] += 1
        top_10_keystore = sorted(top_10_keystore.items(), key = lambda x: x[1], reverse = True)
        reverse_state_keystore = {}
        for k,v in top_10_keystore:
            if v in reverse_state_keystore:
                reverse_state_keystore[v].append(k)
            else:
                reverse_state_keystore[v] = [k]
        for k in reverse_state_keystore:
            reverse_state_keystore[k] = sorted(reverse_state_keystore.get(k))

        if __debug__:
            print("key store for states : ",  reverse_state_keystore)
        return reverse_state_keystore
        

    def save_to_states_file(self, keystore, count, state_filename):
        ### File header : TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        if os.path.isfile(state_filename):
             print("WARNING : File already exists. Overwriting!! " + state_filename)

        state_file_fd = open(state_filename, 'w')
        state_file_fd.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
        written_lines = 0
        for k in keystore:
            percent = (k/count) * 100.00
            str_percent = str(percent) + '%'
            v = keystore.get(k)
            for i in range(len(v)):
                state_file_fd.write("{0};{1};{2}\n".format(v[i],k,str_percent))
                written_lines += 1
                if (written_lines == 10):
                    return
        return

    def __find_col_idx_occupation(self):
        if 'SOC_NAME' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('SOC_NAME')  
        elif 'LCA_CASE_SOC_NAME' in self.h1b_data[0]:
            idx = self.h1b_data[0].index('LCA_CASE_SOC_NAME') 
        if __debug__:
            print("Occupation idx : ", idx, self.h1b_data[0][idx]) 
        return idx   

    def __get_occupations_list(self):
        occupations_list = []
        self.occup_idx = self.__find_col_idx_occupation()
        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                self.h1b_data[i][self.occup_idx] = self.h1b_data[i][self.occup_idx].strip('\"')
                occupations_list.append(self.h1b_data[i][self.occup_idx])
        if __debug__:
            print("total occupations : ", len(occupations_list))
        return occupations_list

    def find_top_occupation(self):
        top_10_keystore = {}
        occupations_list = self.__get_occupations_list()
        for occuapation in occupations_list:
            top_10_keystore[occuapation] = 0

        for i in range(1,len(self.h1b_data)):
            if self.h1b_data[i][2] == "CERTIFIED":
                idx = occupations_list.index(self.h1b_data[i][self.occup_idx])
                top_10_keystore[occupations_list[idx]] += 1
        top_10_keystore = sorted(top_10_keystore.items(), key = lambda x: x[1], reverse = True)
        reverse_state_keystore = {}
        for k,v in top_10_keystore:
            if v in reverse_state_keystore:
                reverse_state_keystore[v].append(k)
            else:
                reverse_state_keystore[v] = [k]
        for k in reverse_state_keystore:
            reverse_state_keystore[k] = sorted(reverse_state_keystore.get(k))

        return reverse_state_keystore

    def save_to_occupations_file(self, keystore, count, occup_filename):
        ## File header : TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        if os.path.isfile(occup_filename):
             print("WARNING : File already exists. Overwriting!! " + occup_filename)
        occup_file_fd = open(occup_filename, 'w')
        occup_file_fd.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
        written_lines = 0
        for k in keystore:
            percent = (k/count) * 100.00
            str_percent = str(percent) + '%'
            v = keystore.get(k)
            for i in range(len(v)):
                occup_file_fd.write("{0};{1};{2}\n".format(v[i],k,str_percent))
                written_lines += 1
                if (written_lines == 10):
                    return
        return        
