import json
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

fig_dir = "../figures/"

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} messages)".format(pct, absolute)

if not os.path.isdir(fig_dir):
    os.mkdir(fig_dir)

with open('../data/result.json', encoding='utf8') as fp:
    data = json.load(fp)

personal_information = data['personal_information']
user_name = personal_information['first_name'] + ' ' + personal_information['last_name']

dfs = [] # List containing dataframe of all chats

# Loop over chats
for chat in data['chats']['list']:
    
    # saved_messages chat is ignored
    if chat['type'] == 'saved_messages':
        continue
    
    chat_name = chat['name']
    print("Chat: {}".format(chat_name))
    
    n_msg = len(chat['messages'])
    
    # Get infos to put in the dataframe
    msg_date = []
    msg_sender = []
    msg_txt = []
    for msg in chat['messages']:
        if msg['type'] == 'message':
            msg_date.append(msg['date'])
            msg_sender.append(msg['from'])
            if msg['text'] is dict:
                print("It happens")
                msg_txt.append(msg['text']['text'])
            else:
                msg_txt.append(msg['text'])

    # Creating the dataframe
    index = pd.to_datetime(msg_date,)
    df = pd.DataFrame({'from':msg_sender, 'text':msg_txt}, index=index)
    df['count'] = 1 # Used to count number of messages (I couldn't find something nicer)
    dfs.append(df)

    # Number of messages by participant
    count = df['from'].value_counts()
    
    # Computing counts
    hourly_count = df['count'].resample('H').count()
    daily_count = df['count'].resample('D').count()
    weekly_count = df['count'].resample('W').count()
    monthly_count = df['count'].resample('M').count()

    # Group by hour
    hourly_groupby_count = df['count'].groupby(df.index.hour).count()
    hourly_groupby_count = hourly_groupby_count.reindex(pd.Index(range(24)), fill_value=0)

    # Group by weekday
    weekday_groupby_count = df['count'].groupby(df.index.weekday).count()
    weekday_groupby_count = weekday_groupby_count.reindex(pd.Index(range(7)), fill_value=0)

    if not os.path.isdir(os.path.join(fig_dir, chat_name)):
        os.mkdir(os.path.join(fig_dir, chat_name))
    if not os.path.isdir(os.path.join(fig_dir, chat_name, "pdf")):
        os.mkdir(os.path.join(fig_dir, chat_name, "pdf"))
    if not os.path.isdir(os.path.join(fig_dir, chat_name, "png")):
        os.mkdir(os.path.join(fig_dir, chat_name, "png"))
    
    # Plotting pie chart
    fig, ax = plt.subplots()
    count.plot.pie(shadow=False,
                   labels=count.index,
                   autopct=lambda pct: func(pct, count),
                   textprops=dict(color="w"))

    ax.set_title("Mail exchange percentage")
    ax.legend(title='Participants', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_xlabel('')
    ax.set_ylabel('')
    fig.savefig(os.path.join(fig_dir, chat_name, "pdf/pie_chart_{}.pdf".format(chat_name)), transparent=True)
    fig.savefig(os.path.join(fig_dir, chat_name, "png/pie_chart_{}.png".format(chat_name)))


    # Plotting counts
    # Hourly
    fig, ax = plt.subplots()
    hourly_count.plot(ax=ax)
    fig.savefig(os.path.join(fig_dir, chat_name, "pdf/hourly_count_{}.pdf".format(chat_name)), transparent=True)
    fig.savefig(os.path.join(fig_dir, chat_name, "png/hourly_count_{}.png".format(chat_name)))

    # Daily
    fig, ax = plt.subplots()
    daily_count.plot(ax=ax)
    fig.savefig(os.path.join(fig_dir, chat_name, "pdf/daily_count_{}.pdf".format(chat_name)), transparent=True)
    fig.savefig(os.path.join(fig_dir, chat_name, "png/daily_count_{}.png".format(chat_name)))

    # Weekly
    fig, ax = plt.subplots()
    weekly_count.plot(ax=ax)
    fig.savefig(os.path.join(fig_dir, chat_name, "pdf/weekly_count_{}.pdf".format(chat_name)), transparent=True)
    fig.savefig(os.path.join(fig_dir, chat_name, "png/weekly_count_{}.png".format(chat_name)))

    # Monthly
    fig, ax = plt.subplots()
    monthly_count.plot(ax=ax)
    fig.savefig(os.path.join(fig_dir, chat_name, "pdf/monthly_count_{}.pdf".format(chat_name)), transparent=True)
    fig.savefig(os.path.join(fig_dir, chat_name, "png/monthly_count_{}.png".format(chat_name)))

    # Plotting groupby counts
    # Hourly
    fig, ax = plt.subplots()
    hourly_groupby_count.plot(ax=ax, kind='bar')
    fig.savefig(os.path.join(fig_dir, chat_name, "pdf/hourly_groupby_count_{}.pdf".format(chat_name)), transparent=True)
    fig.savefig(os.path.join(fig_dir, chat_name, "png/hourly_groupby_count_{}.png".format(chat_name)))
    # Weekday
    fig, ax = plt.subplots()
    weekday_groupby_count.plot(ax=ax, kind='bar')
    fig.savefig(os.path.join(fig_dir, chat_name, "pdf/weekday_groupby_count_{}.pdf".format(chat_name)), transparent=True)
    fig.savefig(os.path.join(fig_dir, chat_name, "png/weekday_groupby_count_{}.png".format(chat_name)))
