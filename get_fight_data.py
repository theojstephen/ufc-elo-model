'''
Elo system assumptions:
fighter performance is normally distributed RV
performance is inferred from wins draws losses and no contests



for fight night in http://ufcstats.com/statistics/events/completed?page=all
    for bout in fight night (bottom up)
        if fighter1 id is not in fighter list
            add fighter
        if fighter2 id is not in fighter list
            add fighter
        add fighters and result to CSV (w/l/d)
'''

import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

options = Options()
options.add_argument("--headless=new")            # modern headless mode
options.add_argument("--window-size=1920,1080")   # real desktop viewport
options.add_argument("--no-sandbox")              # needed in many containers
options.add_argument("--disable-dev-shm-usage")   # avoid /dev/shm crashes in Docker

def get_fight_name_and_urls(): # Gets all UFC events: names and links on ufcstats and writes to csv file

    driver = webdriver.Chrome(options=options)
    driver.get("http://ufcstats.com/statistics/events/completed?page=all")
    sleep(0.5)


    print("Getting UFC Event Names, Event links...")
    event_cards = driver.find_elements(By.CLASS_NAME, "b-link_style_black") # Should switch to CSS_SELECTOR

    with open("fights_urls.csv", mode="w", newline='') as file:
        csv_writer = csv.writer(file)

        csv_writer.writerow(["Name", "Link"]) # Headers
        
        for card in event_cards:
            card_link = card.get_attribute("href")
            card_name = card.text

            data = [card_name, card_link]

            csv_writer.writerow(data)


    print("Finished, saved to fights_urls.csv")
    driver.quit()


def get_all_fights_and_results():
    with open("fights_urls.csv", mode="r") as fights_urls:
        urls_reader = csv.reader(fights_urls)
        header = next(urls_reader)

        with open("all_fights_results.csv", mode="w", newline='') as fights_results:
            results_writer = csv.writer(fights_results)
            results_writer.writerow(["Winner", "Winner id","Loser", "Loser id", "No Contest/Draw"])

            driver = webdriver.Chrome(options=options)

            for row in urls_reader: 
                print(row)
                driver.get(row[1]) # Goes to each event URL
                sleep(0.2) # THIS CAN SOMETIMES CAUSE A LIST INDEX ERROR BECAUSE THE PAGE DOESN'T HAVE ENOUGH TIME TO LOAD, IF CASE JUST RUN AGAIN
                event_fighter_names_ids = driver.find_elements(By.CLASS_NAME, "b-link_style_black")
                event_results = driver.find_elements(By.CLASS_NAME, "b-fight-details__table-col_style_align-top")

                for i in range(len(event_results)):
                    win_fighter_name = event_fighter_names_ids[2 * i].text
                    win_fighter_url_id = event_fighter_names_ids[2 * i].get_attribute("href").split("/")[-1]
                    lose_fighter_name = event_fighter_names_ids[(2 * i) + 1].text
                    lose_fighter_url_id = event_fighter_names_ids[(2 * i) + 1].get_attribute("href").split("/")[-1]
                    if event_results[i].text != "WIN":
                        result = "N"
                    else:
                        result = "Y"

                    data = [win_fighter_name, win_fighter_url_id, lose_fighter_name, lose_fighter_url_id, result]
                    print(data)
                    results_writer.writerow(data)


# Finally, for ease of processing, we re-write the list as descending from the oldest fight to the last
def process_data():
    with open("all_fights_results.csv", "r") as fights_results:
        data = fights_results.readlines()
        data.reverse()
        data = data[:-1] # Remove header which is now at the end
        header = 'Winner, Winner id,Loser, Loser id, No Contest/Draw\n'
        data.insert(0, header)

    with open("all_fights_results_desc.csv", "w") as fights_results:
        fights_results.writelines(data)

if __name__ == "__main__":
    get_fight_name_and_urls()
    get_all_fights_and_results()
    process_data()