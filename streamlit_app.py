import streamlit as st
import heapq
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.firefox import GeckoDriverManager

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

# from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


cloud = True

def generate_transactions(names, amounts):
    assert(len(names) == len(amounts))
    
    winners = []
    losers = []
    
    for i in range(len(names)):
        if amounts[i] > 0:
            winners.append([amounts[i], names[i]])
        else:
            losers.append([amounts[i], names[i]])

    winners.sort()
    losers.sort()
    transactions = []
    
    while(winners):
        biggest_winner = winners[-1]
        smallest_loser = losers[-1]
        amt_to_pay = min(biggest_winner[0], -smallest_loser[0])
        
        transactions.append([biggest_winner[1], smallest_loser[1], amt_to_pay])
        winners[-1][0] -= amt_to_pay
        losers[-1][0] += amt_to_pay
        
        
        if abs(winners[-1][0]) < 0.01:
            winners.pop()
        if abs(losers[-1][0]) < 0.01:
            losers.pop()
        winners.sort()
        losers.sort()
        
        
    
    return transactions


st.markdown('# PokerNow Transaction App')

if 'number_members' not in st.session_state:
    st.session_state['number_members'] = 3
    
if 'member_names' not in st.session_state:
    st.session_state['member_names'] = ['A', 'B', 'C']

if 'amounts' not in st.session_state:
    st.session_state['amounts'] = [120, 260, -380]


website = st.text_input('PokerNow Website')
crawl_website = st.button('Fill From Site')
    
if crawl_website:
    URL = website
    TIMEOUT = 20
    
    if cloud:
        firefoxOptions = Options()
        firefoxOptions.add_argument("--headless")
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(
            options=firefoxOptions,
            service=service,
)
    
    else:
        service = Service(executable_path=ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=service,options=chrome_options)
        
    driver.get(URL)
    driver.implicitly_wait(1)
    content = driver.find_element(By.CSS_SELECTOR, 'button.button-1.show-log-button.small-button.dark-gray')
    content.click()
    ledger = driver.find_element(By.CSS_SELECTOR, 'button.button-1.green-2.small-button.ledger-button')
    ledger.click()
    players = driver.find_elements(By.CSS_SELECTOR, 'td.player-id')
    positive = driver.find_elements(By.CSS_SELECTOR, 'td.positive-net')
    negative = driver.find_elements(By.CSS_SELECTOR, 'td.negative-net')
    
    
    names = []
    amts = []
    for player in players:
        new_name = player.text.split(" @ ")[0]
        names.append(new_name)
    for pos in positive:
        amts.append(int(pos.text))
    for neg in negative:
        amts.append(int(neg.text))
    driver.close()
    st.session_state['number_members'] = len(names)
    st.session_state['member_names'] = names
    st.session_state['amounts'] = amts
    
names = [st.empty() for i in range(st.session_state['number_members'])]
amounts = [st.empty() for i in range(st.session_state['number_members'])]
deletes = [st.empty() for i in range(st.session_state['number_members'])]
    
for i in range(st.session_state['number_members']):
    
    names_col, amounts_col, deletes_col = st.columns(3)

    with names_col:
        name = st.text_input(f'name {i}', value = st.session_state['member_names'][i])
        names[i] = name
        
    with amounts_col:
        amount = st.number_input(f'amount {i}', value = st.session_state['amounts'][i])
        amounts[i] = amount
    with deletes_col:
        delete = st.button(f'delete member {i}')
        deletes[i] = delete
        
st.session_state['member_names'] = names
st.session_state['amounts'] = amounts 

for i in range(st.session_state['number_members']):
    if deletes[i]:
        for j in range(i+1, st.session_state['number_members']):
            st.session_state['member_names'][j-1] = st.session_state['member_names'][j]
            st.session_state['amounts'][j-1] = st.session_state['amounts'][j]
        
        st.session_state['member_names'].pop()
        st.session_state['amounts'].pop()  
        st.session_state['number_members'] -= 1
        st.experimental_rerun()
        
add_button = st.button('add member')

if add_button:
    st.session_state['number_members'] += 1
    st.session_state['member_names'].append('')
    st.session_state['amounts'].append(0)
    st.experimental_rerun()

sum_amounts = sum(amounts)
if sum_amounts > 0.01:
    st.write(f'sum of amounts: {sum_amounts}. Cannot generate transactions when sum is positive.')
elif sum_amounts < -0.01:
    st.write(f'sum of amounts: {sum_amounts}. Cannot generate transactions without distributing excess.')
else:
    st.write(f'sum of amounts: {sum_amounts}')

    generate_transactions_button = st.button('Generate Transaction List')

    if generate_transactions_button:
        transactions = generate_transactions(st.session_state['member_names'], st.session_state['amounts'])
        for trans in transactions:
            st.write(f'{trans[1]} pays {trans[0]} ${trans[2]}')