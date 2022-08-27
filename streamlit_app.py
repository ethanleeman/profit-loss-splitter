import streamlit as st
import heapq

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

st.write('sum of amounts:', sum(amounts))

generate_transactions_button = st.button('Generate Transaction List')

if generate_transactions_button:
    transactions = generate_transactions(st.session_state['member_names'], st.session_state['amounts'])
    for trans in transactions:
        st.write(f'{trans[1]} pays {trans[0]} ${trans[2]}')