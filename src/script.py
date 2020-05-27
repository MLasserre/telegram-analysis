import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

with open('../data/result.json', encoding='utf8') as fp:
    data = json.load(fp)

personal_information = data['personal_information']
user_name = personal_information['first_name'] + ' ' + personal_information['last_name']

chat_names = {}
for i,l in enumerate(data['chats']['list']):
    if 'name' in l.keys():
        chat_names[l['name']] = i

# TODO: loop over chats
chat = data['chats']['list'][1]
n_msg = len(chat['messages'])

msg_sender = []
for msg in chat['messages']:
    if 'from' in msg.keys():
        msg_sender.append(msg['from'])

participants = list(set(msg_sender))
participants.remove(user_name)

n_msg_user = 0
n_msg_contact = 0
for msg in chat['messages']:
    if 'from' in msg.keys():
        if msg['from'] == user_name:
            n_msg_user = n_msg_user + 1
        elif msg['from'] == participants[0]:
            n_msg_contact = n_msg_contact + 1
list_n_msg = [n_msg_user, n_msg_contact]
persons = [user_name] + participants

print('User: {}'.format(n_msg_user))
print('Contact: {}'.format(n_msg_contact))
print('Total: {}'.format(n_msg))
print('Ratios: {}, {}'.format(n_msg_user/n_msg, n_msg_contact/n_msg))

print(chat['messages'][1]['text'])

dates = []
texts = []
for msg in chat['messages']:
    dates.append(msg['date'])
    if msg['text'] is dict:
        texts.append(msg['text']['text'])
    else:
        texts.append(msg['text'])

index = pd.to_datetime(dates)
ts = pd.Series(texts, index=index)
ts.index.name = 'TimeStamp'
count = ts.resample('D').count()

fig, ax = plt.subplots()

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} messages)".format(pct, absolute)


wedges, texts, autotexts = ax.pie(list_n_msg, autopct=lambda pct: func(pct, list_n_msg),
                                  textprops=dict(color="w"))

ax.legend(wedges, persons,
          title="Users",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Mail exchange percentage")

plt.show()

ax.pie([np.round(n_msg_user/n_msg,2)*100, np.round(n_msg_contact/n_msg,2)*100])
plt.show()

fig, ax = plt.subplots()
count.plot(ax=ax)
plt.show()
