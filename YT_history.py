#!/usr/bin/env python
# coding: utf-8

# In[57]:


import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# In[58]:


with open('watch-history.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} watch entries. Nice, you got history!")


# In[59]:


# Cell 3: Turn it into a clean DataFrame
df = pd.DataFrame(data)

# Quick look
df.head(3)


# In[60]:


df.info()


# In[61]:


df.shape


# In[62]:


# Convert to UTC-naive (drops tz but keeps the correct UTC time)
df['time'] = pd.to_datetime(df['time']).dt.tz_localize(None)

# Now these won't warn
df['date']       = df['time'].dt.date
df['month']      = df['time'].dt.to_period('M')
df['year']       = df['time'].dt.year
df['month_name'] = df['time'].dt.strftime('%b %Y')
df['weekday']    = df['time'].dt.day_name()
df['hour']       = df['time'].dt.hour


# In[63]:


df.head()


# In[64]:


df.shape


# In[65]:


df.info()


# In[66]:


df.head()


# In[83]:


def extract_artist(subs):
    # If it's a list and has at least one item
    if isinstance(subs, list) and len(subs) > 0:
        # Get the 'name' key safely (returns 'Unknown' if missing)
        return subs[0].get('name', 'Unknown')
    # If empty list, None, or weird type → Unknown
    return 'Unknown'

# Apply it once → creates clean column
df['artist'] = df['subtitles'].apply(extract_artist)

# Quick check
print(df['artist'].value_counts().head(10))
df[['title', 'subtitles', 'artist']].head(8)   # compare original vs clean


# In[84]:


df.head()


# In[91]:


print(df['artist'].value_counts().head(10))


# In[92]:


df.info()


# In[93]:


# Top 10 clean artists
top_10_artists = df['artist'].value_counts().head(10)
print(top_10_artists)

# Plot it
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.barplot(x=top_10_artists.values, y=top_10_artists.index, palette='magma')
plt.title("Top 10 Channels")
plt.xlabel("Times Watched")
plt.ylabel("Channel")
plt.show()


# In[94]:


# === WATCHES OVER TIME ===
monthly_counts = df.groupby('month').size()
plt.figure(figsize=(12, 5))
monthly_counts.plot(kind='line', marker='o', color='teal')
plt.title('YouTube / Music Watches Per Month')
plt.xlabel('Month')
plt.ylabel('Number of Videos Watched')
plt.grid(True, alpha=0.3)
plt.show()


# In[95]:


df.head()


# In[96]:


df.info()


# In[97]:


top_artists = df['artist'].value_counts().head(15)
print(top_artists)


# In[98]:


plt.figure(figsize=(12, 7))
sns.barplot(x=top_artists.values, y=top_artists.index, palette='rocket')
plt.title('Your Top 15 Artists / Channels (Cleaned)')
plt.xlabel('Number of Watches')
plt.ylabel('Artist')
plt.tight_layout()
plt.show()


# In[99]:


df['video_title'] = df['title'].str.replace(r'^Watched\s*', '', regex=True).str.strip()


# In[100]:


df[['title', 'video_title']].head(10)


# In[107]:


df[['artist', 'video_title']].head(10)


# In[108]:


replay = df['video_title'].value_counts().head(20)

print("=== Top 20 Most Repeated Songs / Videos (Replay Energy) ===\n")
print(replay)


# In[109]:


plt.figure(figsize=(12, 7))
sns.barplot(x=replay.values[:15], y=replay.index[:15], palette='flare')
plt.title('Top 15 Most Repeated Tracks (Raw Titles)')
plt.xlabel('Times Played / Watched')
plt.ylabel('Video Title')
plt.tight_layout()
plt.show()


# In[112]:


df[['date', 'month', 'year', 'month_name', 'weekday', 'hour']].head(10)


# In[113]:


print("Earliest watch:", df['date'].min())
print("Latest watch:", df['date'].max())


# In[114]:


print("\nWatches per month:")
print(df['month_name'].value_counts().sort_index())


# In[115]:


#Daily listening patterns
print(df['weekday'].value_counts().sort_values(ascending=False))


# In[116]:


# Count watches per hour
hour_counts = df['hour'].value_counts().sort_index()

print(hour_counts)

# Plot it
import matplotlib.pyplot as plt
plt.figure(figsize=(10,5))
hour_counts.plot(kind='bar', color='purple')
plt.title('Watches by Hour of Day')
plt.xlabel('Hour (0 = midnight, 23 = 11 PM)')
plt.ylabel('Number of Videos')
plt.grid(axis='y', alpha=0.3)
plt.show()


# In[117]:


import seaborn as sns

# Pivot: rows = hour, columns = weekday, values = count
heatmap_data = df.pivot_table(
    index='hour',
    columns='weekday',
    aggfunc='size',
    fill_value=0
)

# Order weekdays properly
weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
heatmap_data = heatmap_data.reindex(columns=weekday_order)

plt.figure(figsize=(12,8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5)
plt.title('Listening Heatmap: Hour of Day vs Weekday')
plt.ylabel('Hour (0-23)')
plt.xlabel('Weekday')
plt.show()


# In[118]:


monthly_plays = df.groupby('month_name').size().sort_index()

monthly_plays.plot(kind='line', marker='o', figsize=(10,5))
plt.title('Plays per Month')
plt.ylabel('Number of Watches')
plt.grid(True, alpha=0.3)
plt.show()


# In[119]:


# Plays per unique date
daily_plays = df['date'].value_counts().sort_index()
print(daily_plays.head(10))

# If one day has 50+ plays → massive binge day


# In[ ]:




