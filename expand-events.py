# see https://github.com/eyeseast/python-frontmatter
import frontmatter 
import os
import time
import pytz
import glob
import shutil
from datetime import datetime as dt, time as tm, date, timezone, timedelta
from recurrent.event_parser import RecurringEvent
from dateutil import rrule
from colorama import init, Fore, Style

# initialize colorama
init( );  

# set debug True to print intermediate results, verbose for ALL the info
debug = True;
verbose = False;

# set the default timezone
os.environ['TZ'] = 'America/Chicago';
time.tzset( );
tz = pytz.timezone('America/Chicago');

## ------------------------------------------ ##
## ---------- Functions --------------------- ##
## ------------------------------------------ ##

# no valid 'dates' string so harvest the 'performanceList' dates
def harvest_perfomance_dates(event):
  dd = [ ];
  print(Fore.YELLOW + "  WARNING: 'dates' is neither discrete nor recurring!" + Style.RESET_ALL);
  for p in event['performanceList']['performance']:
    pd = p['date'];
    print(Fore.YELLOW + "  WARNING: Discrete performanceList date '%s' will be used." % pd + Style.RESET_ALL);
    dd.append(pd);
  return dd;

# parse a 'dates' string using https://github.com/kvh/recurrent and return a list of equivalent datetime values
# if 'dates' is not present or is not a valid recurring date string, return the localized dates from event['performanceList']
def parse_dates_string(event): 
  dd = [ ];
  keys = event.keys( );

  if 'dates' in keys:
    r = RecurringEvent(now_date=date.today( ));    
    rp = r.parse(event['dates']);

    if rp:
      if debug: print("  dates string '%s' successfully parsed" % event['dates']);
      if debug: print("  recurrence params are:", r.get_params( ));

      # if this is a discrete datetime...
      if isinstance(rp, dt):
        if debug: print("  Parsed event['dates'] is a discrete datetime object");
        lp = tz.localize(rp);
        print(Fore.YELLOW + "  Attention: Discrete date '%s' will be used." % lp + Style.RESET_ALL);
        dd.append(lp);

      # if it's a valid recurring date...
      elif r.is_recurring:
        r = add_one_day_until(rp);
        if debug: print("  this recurring event string is:", r);
        rr = rrule.rrulestr(r);
        for index, recur in enumerate(rr): 
          lp = tz.localize(recur);
          if debug: print("  individual datetime is: ", lp);
          if index == 100:
            if debug: print("WHOA! This recurring dates has generated more than 100 discrete dates.  Are you sure about this?");
            break;
          dd.append(lp);

    else:   # not a discrete date nor recurring... use the 'performanceList' performance dates
      dd = harvest_perfomance_dates(event);

  else:  # not a discrete date nor recurring... use the 'performanceList' performance dates
    dd = harvest_perfomance_dates(event);

  if debug: print("  parse_dates_string returns datetime list:", dd);
  return dd;

# add_one_day_until - Adds a day (24 hours) to any recurring date UNTIL value to make it inclusive
def add_one_day_until(recur_string):
  if debug: print("  incoming recur_string is:", recur_string);      
  if isinstance(recur_string, str):
    if "UNTIL=" in recur_string:
      [junk, until] = recur_string.split("UNTIL=");
      if debug: print("  until is:", until);      
      if until:
        day_after = dt.strptime(until, "%Y%m%d").date( ) + timedelta(days=1);
        recur_string = recur_string.replace(until, day_after.strftime("%Y%m%d"));
  if debug: print("  outgoing recur_string is:", recur_string);      
  return recur_string;

# event_in_the_past - Checks if date or expiryDate has passed and returns True or False
def event_in_the_past(ed):
  if isinstance(ed, dt):
    if not (date.today( ) < ed.date( )):
      if debug: print(Fore.YELLOW + "  datetime event is in the past!" + Style.RESET_ALL);
      return True;
    else:
     return False;
             
  if isinstance(ed, date):
    if not (date.today( ) < ed):
      if debug: print(Fore.YELLOW + "  date event is in the past!" + Style.RESET_ALL);
      return True;
    else:
     return False;
     
  keys = ed.keys( );
  if 'expiryDate' in keys:
    return event_in_the_past(ed['expiryDate']);
  if 'date' in keys:
    return event_in_the_past(ed['date']);

  return False;

# parse_frontmatter - Returns a .md file's full frontmatter content
def parse_frontmatter(filepath):
  md_file = open(filepath, 'r');
  front = frontmatter.load(filepath);
  return front;

## ------------------------------------------ ##
## ----------------- Main ------------------- ##
## ------------------------------------------ ##

shows = './site/content/show/';
pre_shows = './site/content/pre-show/';
data = './site/data/events/';
past = './site/content/event/past/';
active = './site/content/event/active/';

### sweep through event/active and move past events to event/past ###
files = os.listdir(active);

### loop through the files in 'content/event/active' to make check for events that have passed
for filename in files:
  if filename.endswith('.md'):    
    filepath = active + filename;
    if debug: print(Fore.GREEN + 'Active event path is:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'event/active', check if it should be in the past
    event = parse_frontmatter(filepath);

    # if this is a 'draft' event, skip it.
    if event['draft']:
      continue;
    elif event_in_the_past(event['date']):
      if debug: print(Fore.YELLOW + 'Moving active event', filepath, 'to the past' + Style.RESET_ALL);

      # remove expiryDate from the frontmatter and write the result to past 
      if 'expiryDate' in event: del event['expiryDate'];
      if debug and verbose: print(frontmatter.dumps(event));
      with open(past + filename, "w") as f:
        f.write(frontmatter.dumps(event));
      try:
        os.remove(filepath);
      except:
        print(Fore.RED + "Error while deleting file: " + filepath + Style.RESET_ALL);

### loop through the files in 'content/event/active' to make backups ###
for filename in files:  
  if filename.endswith('.md'):    
    filepath = active + filename;
    if debug: print(Fore.GREEN + 'Active event found in:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'event/active', keep it temporarily as a backup
    destination = active + os.path.splitext(filename)[0] + '.bak';  
    try:
      shutil.move(filepath, destination);
      print('  active event', filepath, 'was moved to backup file', destination);
    except:
      print(Fore.YELLOW + "Warning: Could not make backup of file: " + filepath + Style.RESET_ALL);

### process the site/content/show .md files ###
files = os.listdir(shows);

for filename in files:  
  if filename.endswith('.md'):    
    filepath = shows + filename;
    if debug: print(Fore.GREEN + 'Show path is:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'show/', process it
    event = parse_frontmatter(filepath);
    keys = event.keys( );

    # # if we have an audio_selection: key, add an audio: tag and re-write the .mp3 path
    # if 'audio' not in keys:
    #   if 'audio_selection' in keys:
    #     selection = event['audio_selection'];
    #     event['audio'] = "/audio/15/" + selection + ".mp3";
    #     if debug: print(Fore.YELLOW + "  audio_selection: ", selection, " converted to audio: " + Style.RESET_ALL);

    # if this show already has a performanceList, capture the format and note values and re-use them
    if 'performanceList' in keys:
      captured = [ ];
      for p in event['performanceList']['performance']:
        d = p['date'];
        p_keys = p.keys();
        if 'note' in p_keys:
          n = p['note'];
        else:
          n = '';
        if 'format' in p_keys:
          f = p['format'];
        else:
          f = '2D';
        captured.append({'date': d, 'format': f, 'note': n});

    else:
      captured = False;

    # capture the "event_name" portion of the filename, after the '_', for re-use
    [named_date, event_name] = filename.split('_');
    if debug: print("  named_date and event_name are:", named_date, "and", event_name);

    # make the date portion of the filename match the event's 'date' field date
    if 'date' in keys:
      fdate = event['date'];
      correct_path = shows + fdate.strftime("%Y-%m-%d_") + event_name; 
      if (filepath != correct_path):
        if debug: print(Fore.YELLOW + "  filepath and correct_path are:", filepath, "and", correct_path + Style.RESET_ALL);
        os.rename(filepath, correct_path);
        if debug: print(Fore.GREEN + "    File has been renamed to ", correct_path + Style.RESET_ALL);
        filepath = correct_path;

    # parse the 'dates' string and process the results
    r = parse_dates_string(event);
    if r:  # iterate through 'r' adding individual .md files to 'event/active' directory
      performances = [ ];
      for d in r:
        if debug: print("  discrete/expanded datetime is: ", d);
        # if this generated date is not in the past, process it
        if not event_in_the_past(d):
          event['date'] = d;   # update frontmatter 'date' to the last of the generated dates
          active_filename = active + d.strftime("%Y-%m-%d.%H%M_") + event_name;
          if debug and verbose: print(frontmatter.dumps(event));
          with open(active_filename, "w") as f:
            f.write(frontmatter.dumps(event));
          ## add one performance to the frontmatter performanceList
          performances.append({'date': d, 'format': '2D', 'note': ''});

    # ok, if the number of performances is the same as captured, keep the old 'format' and 'note' values
    if performances and captured:
      if len(performances) == len(captured):
        for i, p in enumerate(performances):
          performances[i]['format'] = captured[i]['format'];
          performances[i]['note'] = captured[i]['note'];
        if debug: print(Fore.GREEN + "  Old performance 'format' and 'notes' have been preserved!" + Style.RESET_ALL);
        
    # at the end of the for loop...calculate an expiryDate the day after 'd'
    day_after = d.date( ) + timedelta(days=1);
    expiryDate = day_after;  # .strftime("%Y%m%d");
    if debug: print("  expiryDate is: ", expiryDate);

    # write the calculated expiryDate and performances back into the .md file
    event['expiryDate'] = expiryDate;
    event['performanceList'] = {'performance': performances};
    with open(filepath, "w") as f:
      f.write(frontmatter.dumps(event));

    # copy as a "pre_show"
    if not event_in_the_past(event):
      shutil.copyfile(filepath, pre_shows + filename);

### process the data/events .md files ###
files = os.listdir(data);

for filename in files:  
  if filename.endswith('.md'):    
    filepath = data + filename;
    if debug: print(Fore.GREEN + 'Event path is:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'data/events', process it
    event = parse_frontmatter(filepath);
    keys = event.keys( );
  
    # capture the "event_name" portion of the filename, after the '_', for re-use
    [named_date, event_name] = filename.split('_');
    if debug: print(Fore.GREEN + "  named_date and event_name are:", named_date, "and", event_name + Style.RESET_ALL);

    # make the date portion of the filename match the event's 'date' field date
    if 'date' in keys:
      fdate = event['date'];
      correct_path = data + fdate.strftime("%Y-%m-%d_") + event_name; 
      if (filepath != correct_path):
        if debug: print(Fore.YELLOW + "  filepath and correct_path are:", filepath, "and", correct_path + Style.RESET_ALL);
        os.rename(filepath, correct_path);
        if debug: print(Fore.GREEN + "    File has been renamed to ", correct_path + Style.RESET_ALL);
    
    # parse the 'dates' string and expand it
    r = parse_dates_string(event);

    if r:
      # iterate through 'r' adding individual .md files to 'event/active' directory
      for d in r: 
        if debug: print("  discrete/expanded datetime is: ", d);
        # if this generated date is not in the past make it active
        if not event_in_the_past(d):
          event['date'] = d;
          active_filename = active + d.strftime("%Y-%m-%d.%H%M_") + event_name;
          if debug and verbose: print(frontmatter.dumps(event));
          with open(active_filename, "w") as f:
            f.write(frontmatter.dumps(event));
    
    else:
      if debug: print(Fore.RED + "  parse_dates_string=False so event was ignored" + Style.RESET_ALL);

### process the site/content/pre-show .md files ###
files = os.listdir(pre_shows);

for filename in files:  
  if filename.endswith('.md'):    
    filepath = pre_shows + filename;
    if debug: print(Fore.GREEN + 'Pre-show path is:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'pre-show/', delete it if in the past
    event = parse_frontmatter(filepath);
    if event_in_the_past(event['expiryDate']):
      try:
        os.remove(filepath);
      except:
        print(Fore.RED + "Error while deleting file: " + filepath + Style.RESET_ALL);

# ok, if we got this far with no errors, it's time to delete all the active/*.bak files
fileList = glob.glob(active + '*.bak');
for filePath in fileList:
  try:
    os.remove(filePath);
  except:
    print(Fore.RED + "Error while deleting file: " + filepath + Style.RESET_ALL);
