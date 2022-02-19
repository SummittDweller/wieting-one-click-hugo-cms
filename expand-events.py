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

# parse a 'dates' string using https://github.com/kvh/recurrent and return False
#   or a list of equivalent datatime values
#   returns False if 'dates' is not present or not valid
def parse_dates_string(event):
  d = [ ];
  keys = event.keys( );

  if 'dates' in keys:
    r = RecurringEvent(now_date=date.today( ));    
    rp = r.parse(event['dates']);
    if debug: print("  dates string '%s' successfully parsed" % event['dates']);
    if debug: print("  recurrence params are:", r.get_params( ));
    if not r.is_recurring:
      if debug: print("  attention: NOT a recurring date but a discrete datetime of:", rp);      
      d.append(rp);
    else:
      r = add_one_day_until(rp);
      if debug: print("  this recurring event string is:", r);
      rr = rrule.rrulestr(r);
      for index, recur in enumerate(rr): 
        if debug: print("  individual datetime is: ", recur);
        if index == 100:
          if debug: print("WHOA! This recurring dates has generated more than 100 discrete dates.  Are you sure about this?");
          break;
        d.append(recur);
    if debug: print("  parse_dates_string returns datetime list:", d);
    return d;
  else:
    print(Fore.RED + "  ERROR: No 'dates' string found in this event!" + Style.RESET_ALL);
    return False;

# add_one_day_until - Adds a day (24 hours) to any recurring date UNTIL value to make it inclusive
def add_one_day_until(recur_string):
  if debug: print("  incoming recur_string is:", recur_string);      
  if isinstance(recur_string, str):
    [junk, until] = recur_string.split("UNTIL=");
    if debug: print("  until is:", until);      
    if until:
      day_after = dt.strptime(until, "%Y%m%d").date( ) + timedelta(days=1);
      recur_string = recur_string.replace(until, day_after.strftime("%Y%m%d"));
  if debug: print("  outgoing recur_string is:", recur_string);      
  return recur_string;

# event_in_the_past - Checks if date or expiryDate has passed and returns True or False
def event_in_the_past(event):
  if isinstance(event, dt):
    if not (date.today( ) < event.date( )):
      if debug: print(Fore.YELLOW + "  event is in the past!" + Style.RESET_ALL);
      return True;
  
  else:
    keys = event.keys( );
    if 'date' in keys:
      if not (date.today( ) < event['date'].date( )):
        if debug: print(Fore.YELLOW + "  event is in the past!" + Style.RESET_ALL);
        return True;
    if 'expiryDate' in keys:
      if not (date.today( ) < event['expiryDate']):
        if debug: print(Fore.YELLOW + "  event is in the past!" + Style.RESET_ALL);
        return True;
  
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
data = './site/data/events/';
past = './site/content/event/past/';
active = './site/content/event/active/';

# create backup files...change all of the 'event/active/' .md files to .bak 
files = os.listdir(active);

### sweep through event/active and move past events to event/past ###
files = os.listdir(active);

for filename in files:  
  if filename.endswith('.md'):    
    filepath = active + filename;
    if debug: print(Fore.GREEN + 'Active event path is:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'event/active', check it if should be in the past
    event = parse_frontmatter(filepath);

    if event_in_the_past(event['date']):
      if debug: print(Fore.YELLOW + 'Moving active event', filepath, 'to the past' + Style.RESET_ALL);

      # remove expiryDate from the frontmatter and write the result to past 
      if 'expiryDate' in event: del event['expiryDate'];
      if debug and verbose: print(frontmatter.dumps(event));
      with open(past + filename, "w") as f:
        f.write(frontmatter.dumps(event));
      try:
        os.remove(filePath);
      except:
        print(Fore.RED + "Error while deleting file: " + filepath + Style.RESET_ALL);

### loop through the files in 'content/event/active' to make backups ###
for filename in files:  
  if filename.endswith('.md'):    
    filepath = active + filename;
    if debug: print(Fore.GREEN + 'Active event found in:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'event/active', keep it temporarily as a backup
    destination = active + os.path.splitext(filename)[0] + '.bak';  
    shutil.move(filepath, destination);
    print('  active event', filepath, 'was moved to backup file', destination);

### process the site/content/show .md files ###
files = os.listdir(shows);

for filename in files:  
  if filename.endswith('.md'):    
    filepath = shows + filename;
    if debug: print(Fore.GREEN + 'Show path is:', filepath + Style.RESET_ALL);
    
    # this is a .md file in 'show/', process it
    event = parse_frontmatter(filepath);
    keys = event.keys( );
    
    # if this show already has a performanceList, capture the format and note values and re-use them
    if 'performanceList' in keys:
      captured = [ ];
      for p in event['performanceList']['performance']:
        p_keys = p.keys();
        if 'note' in p_keys:
          n = p['note'];
        else:
          n = False;
        captured.append({'format': p['format'], 'note': n});

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
    
    r = parse_dates_string(event);
    performances = [ ];
        
    if r:  # iterate through 'r' adding individual .md files to 'event/active' directory
      for d in r: 
        if debug: print("  discrete/expanded datetime is: ", d);
        # if this generated date is not in the past, process it
        if not event_in_the_past(d):
          event['date'] = tz.localize(d);
          active_filename = active + d.strftime("%Y-%m-%d.%H%M_") + event_name; 
          if debug and verbose: print(frontmatter.dumps(event));
          with open(active_filename, "w") as f:
            f.write(frontmatter.dumps(event));
          # add one performance to the frontmatter performanceList 
          performances.append({'date': tz.localize(d), 'format': '2D'});
    
      # ok, if the number of performances is the same as caotured, keep the old 'format' and 'note' values
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

    else:
      if debug: print(Fore.RED + "  parse_dates_string=False so event was ignored" + Style.RESET_ALL);

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
          event['date'] = tz.localize(d);
          active_filename = active + d.strftime("%Y-%m-%d.%H%M_") + event_name; 
          if debug and verbose: print(frontmatter.dumps(event));
          with open(active_filename, "w") as f:
            f.write(frontmatter.dumps(event));
    
    else:
      if debug: print(Fore.RED + "  parse_dates_string=False so event was ignored" + Style.RESET_ALL);

# ok, if we got this far with no errors, it's time to delete all the active/*.bak files
fileList = glob.glob(active + '*.bak');
for filePath in fileList:
  try:
    os.remove(filePath);
  except:
    print(Fore.RED + "Error while deleting file: " + filepath + Style.RESET_ALL);






# # now process the site/data/event .md files
# files = os.listdir(data);
# 
# for filename in files:  
#   if filename.endswith('.md'):    
#     filepath = data + filename;
#     if debug: print(Fore.GREEN + 'Event data path is:', filepath + Style.RESET_ALL);
# 
#     # this is a .md file in 'event/', process it
#     event = parse_frontmatter(filepath);
# 
#     ## Removing this behavior 9-Jun-2021. Only discrete, generated events should be in /past/. 
#     ## Files should be manually removed from data/event/ as they expire.
#     ## any site/data/event/*.md files that have passed, move them to the 'past' subdir and skip
#     # if event_in_the_past(event):
#     #   destination = past + filename;
#     #   shutil.move(filepath, destination);
#     #   print("  event was in the past so", filename, "was moved to the 'event/past' directory");
#     #   break;   # skip this event
# 
#     # capture the "event_name" portion of the filename, after the '_', for re-use
#     [named_date, event_name] = filename.split('_');
#     if debug: print("  named_date and event_name are:", named_date, "and", event_name);
# 
#     # parse the event['dates'] string and expand it
#     r = parse_dates_string(event);
#     if r:
#       if debug: print("  parse_dates_string returned an 'r' value of type", type(r));
#     else:
#       if debug: print("  parse_dates_string returned False so this event will be ignored");
#       break;
# 
#     # single event (non-recurring)... add one .md file to the 'event/active' directory
#     if isinstance(r, dt):
#       if debug: print("  this is a discrete datetime event");
#       # add a local date: value to the front matter and to the filename
#       event['date'] = tz.localize(r);
#       active_filename = active + r.strftime("%Y-%m-%d_") + event_name; 
#       if debug and verbose: print(frontmatter.dumps(event));
#       with open(active_filename, "w") as f:
#         f.write(frontmatter.dumps(event));
# 
#     # recurring event... iterate through 'r' adding multiple .md to the 'event/active' directory
#     if isinstance(r, str):
#       r = add_one_day_until(r);
#       if debug: print("  this recurring event string is:", r);
#       rr = rrule.rrulestr(r);
#       for index, recur in enumerate(rr): 
#         if debug: print("  expanded event datetime is: ", recur);
#         if index == 100:
#           if debug: print("WHOA! This recurring event has generated more than 100 discrete dates.  Are you sure about this?");
#           break;
# 
#         # if this generated date is in the past, put the file there too, else it is active
#         if event_in_the_past(recur):
#           dir = past;
#         else:
#           dir = active;
#         event['date'] = tz.localize(recur);
#         active_filename = dir + recur.strftime("%Y-%m-%d.%H%M_") + event_name; 
#         if debug and verbose: print(frontmatter.dumps(event));
#         with open(active_filename, "w") as f:
#           f.write(frontmatter.dumps(event));
# 
#       # ok, if we got this far with no errors, it's time to delete all the active/*.bak files
#       fileList = glob.glob(active + '*.bak');
#       for filePath in fileList:
#         try:
#           os.remove(filePath)
#         except:
#           print("Error while deleting file : ", filePath);



      # for recur in rr.after(dt.now( )):
      #   event['date'] = recur;
      #   active_filename = active + recur.strftime("%Y-%m-%d_") + event_name; 
      #   if debug: print(frontmatter.dumps(event));
        # with open(active_filename, "w") as f:
        #   f.write(frontmatter.dumps(event));

    # >>> rr.after(datetime.datetime(2010, 1, 2))
    # datetime.datetime(2010, 1, 5, 0, 0)
    # >>> rr.after(datetime.datetime(2010, 1, 25))
    # datetime.datetime(2010, 1, 26, 0, 0)

# # convert a UTC datetime to a local (offset aware) datetime.
# def utc_to_local(utc_dt):
#   return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

# # file_not_found - Determine if a corresponding site/content/event/**/?.md exists
# def file_not_found(filename, search_path):
#   target = search_path + '**/' + filename;
#   result = glob.glob(target, recursive=True);
#   if debug: print('Filename is: %s.  Result is %s' % (filename, result));  
#   if len(result) > 0:
#     return 0;
#   return 1
# 
# # get_event_time_string - Returns an event's time-of-day as a local time string, like "19:00:00-05:00" for 7pm. 
# def get_event_time_string(local_dt):
#   [d, t] = local_dt.split("T", 2);
#   return t;

# # get_final_date - Returns an event's date or last recurrence as a local (offset aware) datetime.
# def get_final_date(event):
#   recurring = False;
#   keys = event.keys( );
# 
#   if 'date' in keys:    
#     event_date = event_last = utc_to_local(event['date']);  
#     date_string = event_date.isoformat( );
#     if debug:
#       print('  event_date is: %s' % event_date);
#       print('    as a string: %s' % date_string);
#   else:
#     if debug:
#       print('ERROR: Every event must have a valid date!');
#     return False;
# 
#   if 'lastRecur' in keys:
#     recurring = True;
#     last_string = event['lastRecur'].strftime("%Y-%m-%dT") + get_event_time_string(date_string);
#     if debug:
#       print('  last_string is: %s' % last_string);
#     event_last = dt.strptime(last_string, "%Y-%m-%dT%H:%M:%S%z");
#     if debug:
#       print('  lastRecur as a datetime is: %s' % event_last);
#     if event_date > event_last:
#       event_last = event_date;
#     if debug:
#       print('  last recurrence is: %s' % event_last);
# 
#   return event_last;    
      
# # is_recurring - Returns an True or False to reflect an event's recurrence settings.
# def is_recurring(event):
#   keys = event.keys( );
#   if 'lastRecur' in keys:
#     return True;
#   else:
#     return False;

  # for track in gpx.tracks:
  #   for segment in track.segments:
  #     for point in segment.points:
  #       final_time = point.time;
  # final_local = utc_to_local(final_time);
  # # print('  Final local time is: {0}'.format(final_local));
  # final = final_local.strftime('%Y-%m-%d_%I.%M%p');
  # return final.replace('_0','_').replace('AM','am').replace('PM','pm');


# # get_final_time - Returns a .gpx route's final <time> tag in Apple workout export format
# def get_final_time(filepath):
#   gpx_file = open(filepath, 'r');
#   gpx = gpxpy.parse(gpx_file);
# 
#   for track in gpx.tracks:
#     for segment in track.segments:
#       for point in segment.points:
#         final_time = point.time;
#   final_local = utc_to_local(final_time);
#   # print('  Final local time is: {0}'.format(final_local));
#   final = final_local.strftime('%Y-%m-%d_%I.%M%p');
#   return final.replace('_0','_').replace('AM','am').replace('PM','pm');
# 
# # rename_gpx - Rename the target .gpx file, changing the name based on the last <time> tag value
# def rename_gpx(filepath):
#   workout_time = get_final_time(filepath);
#   new_filename = "route_" + workout_time + ".gpx"
#   # print('  New filename: {0}'.format(new_filename));
#   return new_filename;



    # final = get_final_date(event);

#     new_gpx = rename_gpx(gpx_path);
#     new_path = './static/gpx/' + new_gpx;
#     if gpx_path != new_path:
#       os.replace(gpx_path, new_path);
#       print("Renamed .gpx file '{0}' to '{1}'".format(gpx_path, new_path))
# 
# # Get .gpx files in static/gpx/
# for f_name in os.listdir('./static/gpx/'):
#   if f_name.endswith('.gpx') and f_name.startswith('route_'):
#     gpx_path = './static/gpx/' + f_name;
# 
#     # Create equivalent .md filename  
#     md_name = f_name.replace('route_','').replace('gpx','md');
#     # Check for existing md_name file in contents/hikes/. If found then skip this .gpx
#     md_dir = './content/hikes/';
# 
#     # See if the md_name file exists...
#     if file_not_found(md_name, md_dir):
#       print('No .md file found for {0}. Creating this file now.'.format(md_name));
# 
#       # Process this .gpx, start by turning the filename into different date/time forms
#       date_time_str = md_name.replace('.md','');
#       date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d_%I.%M%p');
# 
#       # Create year/month directory if one does not already exist
#       Ym = date_time_obj.strftime('%Y/%m');
#       new_dir = "./content/hikes/{0}".format(Ym);
#       print("new_dir is: {0}".format(new_dir));
#       os.makedirs(new_dir, exist_ok=True);
#       md_path = new_dir + "/" + md_name;
# 
#       # Calculate the negative "weight" of this new .md file based on the date.
#       weight = "-" + date_time_obj.strftime('%Y%m%d%k%M');
# 
#       # Create year/month directory for the .gpx file if one does not already exist
#       new_dir = "./static/gpx/{0}".format(Ym);
#       print("new_dir is: {0}".format(new_dir));
#       os.makedirs(new_dir, exist_ok=True);
#       new_path = new_dir + "/" + f_name;
#       # Move the .gpx file from the old directory to the new one
#       shutil.move(gpx_path, new_path);
# 
#       title = md_name.replace('.md','').replace('.',':');
#       pubDate, pubTime = title.split('_');
#       lastMod = date_time_obj.isoformat();
# 
#       # Open the new .md file
#       md_file = open(md_path,'x');
#       # Write it line-by-line
#       md_file.write("---\n");
#       md_file.write("title: %s\n" % title);
#       md_file.write("weight: %s\n" % weight);
#       md_file.write("publishDate: %s\n" % pubDate);
#       md_file.write("lastmod: %s\n" % lastMod);
#       md_file.write("location: Toledo, IA\n");
#       md_file.write("highlight: false\n");
#       md_file.write("bike: false\n");
#       md_file.write("trashBags: false\n");
#       md_file.write("trashRecyclables: false\n");
#       md_file.write("trashWeight: false\n");
#       md_file.write("---\n");
# 
#       md_file.write('{{< leaflet-map mapHeight="500px" mapWidth="100%" >}}\n');
#       md_file.write('  {{< leaflet-track trackPath="%s/%s" lineColor="#4b37bf" lineWeight="5" graphDetached=true >}}\n' % (Ym, f_name));
#       md_file.write('{{< /leaflet-map >}}\n');
#       md_file.write(" ");
# 
#       # Close the file
#       md_file.close();
#       print("NEW markdown written to file %s." % md_path); 
#     else:
#       skipped += 1;
#       # print("Markdown file %s already exists and will not be replaced." % md_name);  
# 
# print('All done. %s existing markdown files were NOT replaced.' % skipped);     
      
       
