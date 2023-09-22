import json
from datetime import datetime
from urllib.request import urlopen

from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

# Download the raw statistics from GitHub.
base_url = 'https://raw.githubusercontent.com/pdfo/stats/main/archives/'
conda = json.loads(urlopen(base_url + 'conda.json').read())
github = json.loads(urlopen(base_url + 'github.json').read())
pypi = json.loads(urlopen(base_url + 'pypi.json').read())

# Keep only the mirror-excluded statistics for PyPI.
pypi = [{'date': d['date'], 'downloads': d['downloads']} for d in pypi if d['category'] == 'without_mirrors']

# Combine the daily statistics into a single list.
download_dates = []
daily_downloads = []
for src in [conda, github, pypi]:
    for d in src:
        date = datetime.strptime(d['date'], '%Y-%m-%d').date()
        try:
            # If the date is already in the list, add the downloads.
            i = download_dates.index(date)
            daily_downloads[i] += d['downloads']
        except ValueError:
            # Otherwise, add the date and downloads.
            download_dates.append(date)
            daily_downloads.append(d['downloads'])
daily_downloads = [d for _, d in sorted(zip(download_dates, daily_downloads))]
download_dates = sorted(download_dates)
cumulative_downloads = [sum(daily_downloads[:i]) for i in range(1, len(daily_downloads) + 1)]

# Plot the cumulative downloads.
fig, ax = plt.subplots()
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, p: format(int(y), ',')))
ax.margins(x=0, y=0)
ax.plot(download_dates, cumulative_downloads, color='#4f8d97')
ax.set_title('Cumulative downloads of PDFO')