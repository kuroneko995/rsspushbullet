# Require https://github.com/Azelphur/pyPushBullet
import feedparser
from pushbullet import PushBullet
apiKey = ""

def read_config():
  feeds_file = open("feeds.txt",'r')
  feeds = []
  current_feed = {}

  for line in feeds_file:
    if (line[0] == '#') or (line.isspace()):
      continue
    elif line[0] == '+':
      feeds[-1]["positive"].append(line[1:-1])
    elif line[0] == '-':
      feeds[-1]["negative"].append(line[1:-1])
    elif line.split()[0] == "pushbullet_api":
      global apiKey
      apiKey = line.split()[2]
    else:
      current_feed = dict()
      current_feed["url"] = line[:-1]
      current_feed["positive"] = []
      current_feed["negative"] = []
      feeds.append(current_feed)
         
  feeds_file.close()
  return feeds

def read_log():
  log_file = open("log.txt",'r')
  previous_files = []
  for line in log_file:
    previous_files.append(line[:-1])
  log_file.close()
  return previous_files

def write_log(entries_list):
  log_file = open("log.txt",'a')
  for entry in entries_list:
    log_file.write(entry["title"] + '\n')
  log_file.close()

def push_link(entries_list):
  print apiKey
  client = PushBullet(apiKey)
  for entry in entries_list:
    client.push_link(entry["title"], entry["link"])

def main():
  feeds = read_config()
  previous_titles = read_log()
  new_entries = []
  for feed_info in feeds:
    entries = filter_feed(feed_info)
    for entry in entries:
      if entry["title"] not in previous_titles:
        new_entries.append(entry)
        print "New file found", entry["title"]

  push_link(new_entries)
  write_log(new_entries)

def filter_feed(feed_info):
  new_entries = []
  feed = feedparser.parse(feed_info["url"])
  for entry in feed["entries"]:
    is_valid = True
    title = entry["title"]
    for keyword in feed_info["positive"]:
      if keyword not in title:
        is_valid = False
        break
    if not is_valid:
      continue
    for keyword in feed_info["negative"]:
      if keyword in title:
        is_valid = False
        break
    if is_valid:
      new_entries.append(entry)

  return new_entries
    
main()
