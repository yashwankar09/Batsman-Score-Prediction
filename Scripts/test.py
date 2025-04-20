from bs4 import BeautifulSoup
import requests
from web_scapper import Extactor
# from batting_data_clean import processFile
from bowling_data_clean import processFile

processFile(r"D:\Yash\Projects\IPL-2024\CSV Data\bowling\bowler_data_45th_Match_D_N_.csv")


link = ' https://www.espncricinfo.com/series/indian-premier-league-2023-1345038/lucknow-super-giants-vs-chennai-super-kings-45th-match-1359519/full-scorecard'
# link = 'https://www.espncricinfo.com/series/indian-premier-league-2024-1410320/rajasthan-royals-vs-royal-challengers-bengaluru-eliminator-1426310/full-scorecard'

source_url = requests.get(link).text

soup = BeautifulSoup(source_url,'lxml')

team_names = soup.find('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate')
first_inning_team_name = team_names.text
second_inning_team_name = team_names.find_next('span',class_='ds-text-tight-l ds-font-bold ds-text-typo hover:ds-text-typo-primary ds-block ds-truncate').text
print(second_inning_team_name)

# ext = Extactor(link=link)

# try:
#     ext.run()
# except Exception as e:
#     print(e)
#104
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i: i+n]
    return l

try:
    first_inn = soup.find('div',class_ = 'ds-rounded-lg ds-mt-2') #data for first inning team.
    data = soup.find('div',class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3').text.split(',')
    match_id = data[0]
    toss_winner_all = soup.find('td',class_='ds-text-typo')
    first_inning_team_name = first_inn.find('span',class_='ds-text-title-xs ds-font-bold ds-capitalize').text
    try:
        second_inn = first_inn.nextSibling    # second innings data
        second_inning_team_name = second_inn.find('span',class_='ds-text-title-xs ds-font-bold ds-capitalize').text
    except Exception as e:
        second_inn = None
        print('Second Inning data not present',e)
except Exception as e:
    print('First Inning data not present',e)

if first_inn is not None and soup is not None:
    try:
        # self.data = soup.find('div',class_='ds-text-tight-m ds-font-regular ds-text-typo-mid3').text.split(',')
        # toss_winner_all = soup.find('td',class_='ds-text-typo')
        toss_winner = toss_winner_all.find_next('span',class_='ds-text-tight-s ds-font-regular').text
        win_by = soup.find('p',class_='ds-text-tight-s ds-font-medium ds-truncate ds-text-typo').text
        #potm = soup.find('span',class_='ds-text-tight-m ds-font-medium ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block ds-cursor-pointer').text                
        extra_runs = first_inn.find('td',class_='ds-min-w-max ds-text-right').text
        team_name = first_inn.find('span',class_='ds-text-title-xs ds-font-bold ds-capitalize').text #retrives team name inning wise.
        print(extra_runs,team_name,win_by,toss_winner)
        # self.match_id = self.data[0]
        # match_id = self.data[0]
    except Exception as e:
        print('First Innings data present. Problem while fetch the metadata.',e)

if second_inn is not None:
    for i in second_inn.children:
        batsman_list = []
        batters = i.find_all('td',class_=['ds-w-0 ds-whitespace-nowrap ds-min-w-max',
                                            'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-border-line-primary ci-scorecard-player-notout'])

        for batter in batters:
            batsman_list.append(batter.text)

    stats = i.find_all('td',class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')
    # Filter out those that contain an `i` tag with the specified class
    # filtered_divs = [
    #     div for div in stats
    #     if not div.find('i', class_='icon-play_circle-outlined ds-text-icon-primary ds-cursor-pointer ds-flex')
    # ]

    # filtered_divs = [
    #     div for div in stats
    #     if div.find('td', class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right') or
    #        div.find('td', class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right').get_text(strip=True)
    # ]

    nonelist = []
    for ele in stats:
        if ele.text == '':
            pass
        else:
            nonelist.append(ele.text)

    # print(nonelist)

    # table = i.find('table', class_='ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table')

    # # Find all <td> elements within this table
    # td_elements = table.find_all('td', class_='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right')

    # # Count the total number of <td> elements found
    # td_count = len(td_elements)
    # print(td_count)

    # print(f"Total number of <td> elements: {total_td}")
    # # Now `filtered_divs` will contain only the `div` elements you want
    # # for div in filtered_divs:
    # #     print(div.get_text(),end=' ')

    stats_lst_bat = []
    stats_lst_ball = []

    # runs = i.find_all('td',class_ = 'ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo')
    # runs_list = []
    # for ff in runs:
    #     runs_list.append(ff.text)

    for run in nonelist:
        stats_lst_bat.append(run)
        stats_lst_ball.append(run)

    # print(stats_lst_bat)
    # print(len(stats_lst_bat))

    stats_final_list = list(divide_chunks(stats_lst_bat,5))
    print(stats_final_list[0][4])
    if '.' in stats_final_list[0][4]:
        print('yes')  
    else:
        stats_final_list = list(divide_chunks(stats_lst_bat,4))

        for lst in range(len(batsman_list)):
            stats_final_list[lst].insert(1,0)
            

        print('no')
    print(stats_final_list)
    # print(len(stats_final_list))

    bowler_that_got_batsman_out = i.find_all('span',class_='ds-flex ds-cursor-pointer ds-items-center')
    bowler_that_got_batsman_out_list = []
    for bowler in bowler_that_got_batsman_out:
        bowler_that_got_batsman_out_list.append(bowler.text.split(' b ',1)[-1])