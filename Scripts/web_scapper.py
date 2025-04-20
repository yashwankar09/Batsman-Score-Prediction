from bs4 import BeautifulSoup
import requests
from csv_ops import Operations
import pandas as pd
import re

class Extactor():

    def __init__(self,link):
        self.link = link
        self.links = []
        self.soup = None

        try:
            with open(self.link,'r+',) as f:
                [self.links.append(line.strip()) for line in f.readlines()]
        except:
            self.links.append(self.link)

    def initSOUP(self,soup=None):
        self.soup = soup
        # return self.soup if self.soup is not None else None

    def divide_chunks(self,l, n):
        for i in range(0, len(l), n):
            yield l[i: i+n]
        return l
            
    def getUniqueElements(self,list1,list2):
        # Find unique elements
        unique_in_list1 = [item for item in list1 if item not in list2]
        unique_in_list2 = [item for item in list2 if item not in list1]
        
        # Combine the results
        unique_elements = unique_in_list1 + unique_in_list2
        return unique_elements[1:]
    
    def replace_special_characters(self,input_string):
        return re.sub(r'[^a-zA-Z0-9]+', '_', input_string)
    
    def abandonedDetails(self,check_first_inn,check_second_inn):

        self.match_data = self.soup.find('div',class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3').text.split(',')
        
        self.match_id = self.match_data[0]
        self.match_id_n = self.replace_special_characters(self.match_id)
        self.match_date = self.match_data[-3]+''+self.match_data[-2]
        self.venue = self.match_data[1]
        team_names = self.soup.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate')
        self.first_inning_team_name = team_names.text
        self.second_inning_team_name = team_names.find_next('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate').text

        # batPath = r'D:\Yash\Projects\IPL-2024\CSV Data\no result\batsman_data_{}.csv'.format(self.match_id_n)
        # ballPath = r'D:\Yash\Projects\IPL-2024\CSV Data\no result\bowler_data_{}.csv'.format(self.match_id_n)
        # etrPath = r'D:\Yash\Projects\IPL-2024\CSV Data\no result\extra_runs_{}.csv'.format(self.match_id_n)
        # potmPath = r'D:\Yash\Projects\IPL-2024\CSV Data\no result\potm_data_{}.csv'.format(self.match_id_n)

        # self.bowler_dict = {}
        # self.batsman_dict = {}
        # self.potm_dict = {}
        # self.extra_run_dict = {}
        # self.batsman_dict = {'id':[self.match_id],'batsman':['-'],'wicket_by':['-'],'stats':['-'],'batting_team':['-'],'bowling_team':['-'],'date':[self.match_date],'venue':[self.venue],
        #                     'winner':['Match Abadoned'],'toss':['-'],'runs_scored':[0]}
        if check_first_inn is None:

            self.batsman_data = []
            self.bowler_data = []
            self.potm_list = []
            self.extra_run_list = []

            str1 = self.match_id,'-','-',['0','0','0','0','0.00'],self.first_inning_team_name,self.second_inning_team_name,self.match_date,self.venue,'No result','-',0
            self.batsman_data.append(list(str1))
            str2 = self.match_id,'-','-',['0','0','0','0','0.00'],self.second_inning_team_name,self.first_inning_team_name,self.match_date,self.venue,'No result','-',0
            self.batsman_data.append(list(str2))

            str1 = self.match_id,'-','-',['0','0','0','0','0','0','0','0','0'],self.first_inning_team_name,self.second_inning_team_name,self.match_date,self.venue,'No result','-'
            self.bowler_data.append(list(str1))
            str2 = self.match_id,'-','-',['0','0','0','0','0','0','0','0','0'],self.second_inning_team_name,self.first_inning_team_name,self.match_date,self.venue,'No result','-'
            self.bowler_data.append(list(str2))

            str = self.match_id,'-','-'
            self.potm_list.append(list(str))

            str = self.match_id,0,'-'
            self.extra_run_list.append(list(str))

            self.createCSVFiles(match_id=self.match_id)
            self.appendData()

            # self.batsman_dict ={'id':[self.match_id],'date':[self.match_date],'season':[2024],'batsman':['-'],'runs_scored':[0],'balls played':[0],'minutes while batting':[0],'4s':[0],'6s':[0]	
            # ,'s/r':[0],'wicket_by':['-'],'is_notout':[0],'is_out':[0],'is_runout':[0],'batting_team':[self.first_inning_team_name],'bowling_team':[self.second_inning_team_name],
            # 'venue':[self.venue],'day/night':['-'],'captain':['-'],'toss winner':['-'],'toss decision':['-'],'winner':['Match Abadoned'],'win_by':['-'],'summary':['-']}
            
            # self.bowler_dict = {'id':[self.match_id],'date':[self.match_date],'season':[2024],'bowler':['-'],'wicket':[0],'overs':[0],'maidan':[0],'runs':[0],'Econ':[0]	
            # ,'0s_conceded':[0],'4s_conceded':[0],'6s_conceded':[0],'wide_balls':[0],'no_balls':[0],'batting_team':[self.first_inning_team_name],'bowling_team':[self.second_inning_team_name],
            # 'venue':[self.venue],'day/night':['-'],'toss winner':['-'],'toss decision':['-'],'winner':['Match Abadoned'],'win_by':['-'],'summary':['-']}
            
            
            # self.potm_dict = {'id':[self.match_id],'player':['-'],'team':['-']}
            
            # self.extra_run_dict = {'id':[self.match_id],'runs':[0],'batting_team':['-']}

            # bat = pd.DataFrame(self.batsman_dict)
            # ball = pd.DataFrame(self.bowler_dict)
            # potm = pd.DataFrame(self.potm_dict)
            # extra_r = pd.DataFrame(self.extra_run_dict)

            # bat.to_csv(batPath,index=False)
            # ball.to_csv(ballPath,index=False)
            # extra_r.to_csv(etrPath,index=False)
            # potm.to_csv(potmPath,index=False)

        else:
            self.bat_dummy_list = self.match_id,'-','-',['0','0','0','0','0.00'],self.second_inning_team_name,self.first_inning_team_name,self.match_date,self.venue,'No result','-',0
            self.ball_dummy_list = self.match_id,'-',0,['0','0','0','0','0','0','0','0','0'],self.second_inning_team_name,self.first_inning_team_name,self.match_date,self.venue,'No result','-'

        print('Match details were not present, created the dummy match data')
            
    def getInningsObject(self):
        soup = self.soup
        self.first_inn = None
        self.second_inn = None
        self.bat_dummy_list = ''
        self.ball_dummy_list = ''
        
        try:
            self.first_inn = soup.find('div',class_ = 'ds-rounded-lg ds-mt-2') #data for first inning team.
            self.data = soup.find('div',class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3').text.split(',')
            self.win_by = soup.find('p',class_='ds-text-tight-s ds-font-medium ds-truncate ds-text-typo').text
            self.match_id = self.data[0]
            self.toss_winner_all = soup.find('td',class_='ds-text-typo')
            self.first_inning_team_name = self.first_inn.find('span',class_='ds-text-title-xs ds-font-bold ds-capitalize').text
            try:
                self.second_inn = self.first_inn.nextSibling    # second innings data
                self.second_inning_team_name = self.second_inn.find('span',class_='ds-text-title-xs ds-font-bold ds-capitalize').text
            except Exception as e:
                self.second_inn = None
                team_names = self.soup.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate')
                #self.first_inning_team_name = team_names.text
                self.second_inning_team_name = team_names.find_next('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate').text
                print('Second Inning data not present')
                self.abandonedDetails(self.first_inn,self.second_inn)
        except Exception as e:
            self.abandonedDetails(self.first_inn,self.second_inn)
            print('First Inning data not present')

        return self.first_inn,self.second_inn
    
    def getMatchMetadata(self,inning_object=None):
        soup = self.soup
        if self.first_inn is not None and soup is not None:
            try:
                # self.data = soup.find('div',class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3').text.split(',')
                # toss_winner_all = soup.find('td',class_='ds-text-typo')
                self.toss_winner = self.toss_winner_all.find_next('span',class_='ds-text-tight-s ds-font-regular').text
                self.team_name = inning_object.find('span',class_='ds-text-title-xs ds-font-bold ds-capitalize').text #retrives team name inning wise.
                self.extra_runs = inning_object.find('td',class_='ds-min-w-max ds-text-right').text
                self.potm = soup.find('span',class_='ds-text-tight-m ds-font-medium ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block ds-cursor-pointer').text
                # self.match_id = self.data[0]
                # match_id = self.data[0]
            except:
                self.potm = '-'
                print('First Innings data present. Problem while fetch the metadata.')

    def inningsData(self,inning_object): 
        #****************************************** BATTING DATA ******************************************

        for i in inning_object.children:
            self.batsman_list = []
            batters = i.find_all('td',class_=['ds-w-0 ds-whitespace-nowrap ds-min-w-max',
                                                'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-border-line-primary ci-scorecard-player-notout'])

            for batter in batters:
                if batter.text == '\xa0':
                    pass
                else:
                    self.batsman_list.append(batter.text)

        stats = i.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')
        self.stats_lst_bat = []
        self.stats_lst_ball = []

        self.stats_non_empty = []
        for ele in stats:
            if ele.text == '':
                pass
            else:
                self.stats_non_empty.append(ele.text)

        runs = i.find_all('td',class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo')
        self.runs_list = []
        for ff in runs:
            self.runs_list.append(ff.text)

        for run in self.stats_non_empty:
            self.stats_lst_bat.append(run)
            self.stats_lst_ball.append(run)

        self.stats_final_list = list(self.divide_chunks(self.stats_lst_bat,5))
        if '.' in self.stats_final_list[0][4]:
            pass
        else:
            self.stats_final_list = list(self.divide_chunks(self.stats_lst_bat,4))

            for lst in range(len(self.batsman_list)):
                self.stats_final_list[lst].insert(1,'0')

        # for ele in self.stats_final_list:
        #     print(len(ele))

        bowler_that_got_batsman_out = i.find_all('span',class_='ds-flex ds-cursor-pointer ds-items-center')

        self.bowler_that_got_batsman_out_list = []
        for bowler in bowler_that_got_batsman_out:
            self.bowler_that_got_batsman_out_list.append(bowler.text.split(' b ',1)[-1])

        #****************************************** BOWLING DATA ******************************************

        for i in inning_object.children:
            self.bowler_first_inn_list = []
            bowler_first_inn = inning_object.find_all('div','ds-flex ds-items-center')
            for bowler in bowler_first_inn:
                self.bowler_first_inn_list.append(bowler.text)

        self.bowler_list_final = self.getUniqueElements(list1=self.batsman_list,list2=self.bowler_first_inn_list)
        self.bowler_list_final.reverse()
        # print(self.bowler_list_final)

        self.stats_lst_ball.reverse()
        self.bowler_stat_final = list(self.divide_chunks(self.stats_lst_ball,9))

        self.bowler_first_inn_wickets_list = []
        bowler_first_inn_wickets = inning_object.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-text-right')
        for wickets in bowler_first_inn_wickets:
            self.bowler_first_inn_wickets_list.append(wickets.text)

        self.bowler_first_inn_wickets_list.reverse()

        #****************************************** MATCH DETIALS ******************************************
        self.match_date = self.data[-3]+''+self.data[-2]
        self.venue = self.data[1]

        #****************************************** Extra Runs & POTM DETIALS ******************************************
                
        self.potm_list = []
        self.extra_run_list = []


        potm_str = self.match_id,self.potm,self.win_by
        self.potm_list.append(list(potm_str))

        extra_runs_str = self.match_id,self.extra_runs,self.team_name
        self.extra_run_list.append(list(extra_runs_str))

    def storeData(self):

        self.batsman_data = []
        self.bowler_data = []

        if len(self.bat_dummy_list) != 0:
            self.batsman_data.append(list(self.bat_dummy_list))
        if len(self.ball_dummy_list) != 0:
            self.bowler_data.append(list(self.ball_dummy_list))

        if self.team_name == self.first_inning_team_name:
            self.batting_team = self.first_inning_team_name
            self.bowling_team = self.second_inning_team_name
        else:
            self.bowling_team = self.first_inning_team_name
            self.batting_team = self.second_inning_team_name

        try:
            i = 0
            for i in range(len(self.batsman_list)):
                str = self.match_id,self.batsman_list[i],self.bowler_that_got_batsman_out_list[i],self.stats_final_list[i],self.batting_team,self.bowling_team,self.match_date,self.venue,self.win_by,self.toss_winner,self.runs_list[i]
                self.batsman_data.append(list(str))
        except:
            for j in range(i,len(self.batsman_list)):
                str1 = self.match_id,self.batsman_list[j],' - ',self.stats_final_list[j],self.batting_team,self.bowling_team,self.match_date,self.venue,self.win_by,self.toss_winner,self.runs_list[j]
                self.batsman_data.append(list(str1))

        for rows in range(len(self.bowler_list_final)):
            str = self.match_id,self.bowler_list_final[rows],self.bowler_first_inn_wickets_list[rows],self.bowler_stat_final[rows],self.batting_team,self.bowling_team,self.match_date,self.venue,self.win_by,self.toss_winner
            self.bowler_data.append(list(str))

    def createCSVFiles(self,match_id):
        header_batsman_file = ['id','batsman','wicket_by','stats','batting_team','bowling_team','date','venue','winner','toss','runs_scored']
        header_bowler_file = ['id','bowler','wicket','stats','batting_team','bowling_team','date','venue','winner','toss']
        header_potm_file = ['id','player','team']
        header_extraruns_file = ['id','runs','batting_team']

        self.batPath = r'D:\Yash\Projects\IPL-2024\CSV Data\batting\batsman_data_{}.csv'.format(match_id)
        self.ballPath = r'D:\Yash\Projects\IPL-2024\CSV Data\bowling\bowler_data_{}.csv'.format(match_id)
        self.etrPath = r'D:\Yash\Projects\IPL-2024\CSV Data\extra runs\extra_runs_{}.csv'.format(match_id)
        self.potmPath = r'D:\Yash\Projects\IPL-2024\CSV Data\potm\potm_data_{}.csv'.format(match_id)

        ops = Operations(self.batPath,header_batsman_file)
        ops.createCSVFiles()
        ops = Operations(self.ballPath,header_bowler_file)
        ops.createCSVFiles()
        ops = Operations(self.potmPath,header_potm_file)
        ops.createCSVFiles()
        ops = Operations(self.etrPath,header_extraruns_file)
        ops.createCSVFiles()

    def appendData(self):
        ops = Operations(self.batPath,self.batsman_data)
        ops.appendData()
        ops = Operations(self.ballPath,self.bowler_data)
        ops.appendData()
        ops = Operations(self.potmPath,self.potm_list)
        ops.appendData()
        ops = Operations(self.etrPath,self.extra_run_list)
        ops.appendData()

    def run(self):

        for link in self.links:
            source_url = requests.get(link).text
            try:
                soup = BeautifulSoup(source_url,'lxml')
                self.initSOUP(soup=soup)
                first_inn,second_inn = self.getInningsObject()
                m_ID = self.replace_special_characters(self.match_id)
                if first_inn is not None:
                    self.getMatchMetadata(inning_object=first_inn)
                    self.createCSVFiles(match_id=m_ID)
                    self.inningsData(first_inn)
                    self.storeData()
                    self.appendData()

                if second_inn is not None:
                    self.getMatchMetadata(inning_object=second_inn)
                    self.inningsData(second_inn)
                    self.storeData()
                    self.appendData()
 
                print(m_ID,'Completed.')
            except Exception as e:
                print(f'Please check URL {link}',e)
                self.soup = None
