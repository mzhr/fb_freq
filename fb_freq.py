import sys
import re
import numpy
from matplotlib import pyplot

# Choose correct html parser library
version = sys.version_info.major
if version == 2:
	from HTMLParser import HTMLParser
else:
	from html.parser import HTMLParser

### Initialize Data Structures ###

# Set Month Data Array and Name values.
month = [0] * 12
month_names = [
	"Jan", 
	"Feb", 
	"March",
	"April", 
	"May", 
	"June", 
	"July", 
	"Aug", 
	"Sep", 
	"Oct", 
	"Nov", 
	"Dec"
]

# Set Day Data Array and Name values.
day = [0] * 7
day_names = [
	"Monday", 
	"Tuesday", 
	"Wednesday", 
	"Thursday", 
	"Friday", 
	"Saturday", 
	"Sunday"
]

# Set Time Data Array and Name values.
time = [0] * 24
time_names = []
for name in range(24):
	if name < 10:
		time_names.append("0" + str(name) + ":")
	else:
		time_names.append(str(name) + ":")
for i in range(len(time_names)):
	time_names[i] = time_names[i][:-1]


### Setup and Activate Parser/Data Gatherer ###

# Parse Data while adding to data arrays with regex.
class MessagesParser(HTMLParser):
	def handle_data(self, data):
		match = re.search(
			"(Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday|Friday)(,) " \
			"[0-9]{2} (January|February|March|April|May|June|" \
			"July|August|September|October|November|December) " \
			"[0-9]{4} at [0-9]{2}:[0-9]{2}", data)
		if match:
			for i in range(12):
				if re.search(month_names[i], match.group(0)):
					month[i] = month[i] + 1
			for i in range(7):
				if re.search(day_names[i], match.group(0)):
					day[i] = day[i] + 1
			for i in range(24):
				if re.search(time_names[i], match.group(0)):
					time[i] = time[i] + 1

# Activate Parser on the messenger HTML data file.
file = open("html/messages.htm", 'r')
messages = file.readlines()
parser = MessagesParser()
for i in range(len(messages)):
	parser.feed(messages[i])


### Create Graphs ###

# Bar Graph creater function.
def messages(n_groups, bar_width, x_lim, items, names, 
		x_label, y_label, title, file_name):

	# Plot Graph.
	fig, ax = pyplot.subplots()
	index = numpy.arange(n_groups)
	rects1 = pyplot.bar(index, items, bar_width)
	
	# Add texts and lables.
	pyplot.xlabel(x_label)
	pyplot.ylabel(y_label)
	pyplot.title(title)

	# Shape Graph.
	pyplot.xticks(index + bar_width/2, names)
	pyplot.xlim([min(index) - x_lim, max(index) + x_lim])
	pyplot.tight_layout()

	# Export Graph.
	pyplot.savefig(file_name)


# Create Bar Graph for messenger month frequency.
messages(12, 0.3, 1, month, month_names, "Month of Message Sent", 
	"Number of Messages Sent", "Amount of Messages Sent on that Month", 
	"messages_month.png")

# Create Bar Graph for messenger dag frequency.
messages(7, 0.35, 0.5, day, day_names, "Day of Message Sent", 
	"Number of Messages Sent", "Amount of Messages Sent on Days of the Week", 
	"messages_days.png")

# Create Bar Graph for messenger time frequency.
messages(24, 0.20, 0.5, time, time_names, "Time of message sent", 
	"Number of messages sent", "Amount of Messages Sent on Time of the Day", 
	"messages_times.png")

