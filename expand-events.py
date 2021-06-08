# see https://github.com/eyeseast/python-frontmatter
import frontmatter 
import os
import time
import glob
import shutil
from datetime import datetime as dt, time as tm, timezone

# set debug True to print intermediate results
debug = True;

# set the default timezone
os.environ['TZ'] = 'America/Chicago';
time.tzset( );

# convert a UTC datetime to a local (offset aware) datetime.
def utc_to_local(utc_dt):
  return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

# file_not_found - Determine if a corresponding site/content/event/**/?.md exists
def file_not_found(filename, search_path):
  target = search_path + '**/' + filename;
  result = glob.glob(target, recursive=True);
  if debug:
    print('Filename is: %s.  Result is %s' % (filename, result));  
  if len(result) > 0:
     return 0;
  return 1

# get_event_time_string - Returns an event's time-of-day as a local time string, like "19:00:00-05:00" for 7pm. 
def get_event_time_string(local_dt):
  [d, t] = local_dt.split("T", 2);
  return t;
  
# parse_event - Returns an event's full "event" data structure
def parse_event(filepath):
  if debug:
    print('Event filepath is: %s' % filepath);
  event_file = open(filepath, 'r');
  event = frontmatter.load(filepath);
  return event;

# get_final_date - Returns an event's date or last recurrence as a local (offset aware) datetime.
def get_final_date(event):
  recurring = False;
  keys = event.keys( );
  
  if 'date' in keys:    
    event_date = event_last = utc_to_local(event['date']);  
    date_string = event_date.isoformat( );
    if debug:
      print('  event_date is: %s' % event_date);
      print('    as a string: %s' % date_string);
  else:
    if debug:
      print('ERROR: Every event must have a valid date!');
    return False;
    
  if 'lastRecur' in keys:
    recurring = True;
    last_string = event['lastRecur'].strftime("%Y-%m-%dT") + get_event_time_string(date_string);
    if debug:
      print('  last_string is: %s' % last_string);
    event_last = dt.strptime(last_string, "%Y-%m-%dT%H:%M:%S%z");
    if debug:
      print('  lastRecur as a datetime is: %s' % event_last);
    if event_date > event_last:
      event_last = event_date;
    if debug:
      print('  last recurrence is: %s' % event_last);

  return event_last;    
      
# is_recurring - Returns an True or False to reflect an event's recurrence settings.
def is_recurring(event):
  keys = event.keys( );
  if 'lastRecur' in keys:
    return True;
  else:
    return False;

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

## Main ##

# First pass, move any site/content/event/**/*.md files that have passed--both date AND lastRecur are in the past--to the site/content/event/past directory.
for f_name in os.listdir('./site/content/event/'):
  if f_name.endswith('.md'):
    md_path = './site/content/event/' + f_name;
    event = parse_event(md_path)
    final = get_final_date(event);

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
      
       
