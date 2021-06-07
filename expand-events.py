# see https://github.com/eyeseast/python-frontmatter
import frontmatter 
import os
import time
import glob
import shutil
from datetime import datetime, timezone

os.environ['TZ'] = 'America/Chicago';
time.tzset( );

skipped = 0;

def utc_to_local(utc_dt):
  return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

# file_not_found - Determine if a corresponding site/content/event/**/?.md exists
def file_not_found(filename, search_path):
  target = search_path + '**/' + filename;
  result = glob.glob(target, recursive=True);
  # print('Filename is: %s.  Result is %s' % (filename, result));  
  if len(result) > 0:
     return 0;
  return 1

# get_final_date - Returns an event's final date or lastRecur
def get_final_date(filepath):
  event_file = open(filepath, 'r');
  event = frontmatter.load(filepath);
  final = event['date'];
  print('date is: %s' % final);
  last = event['lastRecur'];
  print('lastRecur is: %s' % last);
  
  # for track in gpx.tracks:
  #   for segment in track.segments:
  #     for point in segment.points:
  #       final_time = point.time;
  # final_local = utc_to_local(final_time);
  # # print('  Final local time is: {0}'.format(final_local));
  # final = final_local.strftime('%Y-%m-%d_%I.%M%p');
  # return final.replace('_0','_').replace('AM','am').replace('PM','pm');
  
  return;


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
    get_final_date(md_path);

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
      
       
