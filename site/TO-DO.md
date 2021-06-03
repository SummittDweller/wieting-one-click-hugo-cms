# Wieting Theatre TODO Development List

## Complete List

  - [x] Add a Donate Menu Item
  - [ ] Automated Creation of TBD Shows and Performances
  - [ ] Add Google, or Other, Calendar Page(s)
  - [x] Add Donor Recognition Text to the Home Page
  - [ ] Add a Pop-Up Notification "Overlay" to the Home Page
  - [x] Add display of Official URL and IMDB URL to the show's page
  - [x] Add a new "Camps" page under "About"
  - [x] Add a "Links" page with a list of external resources. No menu required.
  - [x] Add a "Network" page to document connections. No menu required.
  
## Add a `Donate` Menu Item

In our old site, still running at https://wieting.TamaToledo.org, you will find a `Donate!` menu item.  You can jump directly to it at https://wieting.tamatoledo.org/content/donate-today.  We need the same menu item and page added to the main menu in the new site, complete with a [Donate online - One-time or monthly!](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=E28RAEFST2Z7Q) link as seen in the old page.

_Note:_ Rather than adding this to the menu, I've proposed adding a new brightly colored "Donate!" button to the left of our social media (_Facebook_, _Twitter_, and _Email_) buttons near the top of the home page.

## Automated Creation of TBD Shows and Performances

The new site now has two content types for events, namely `show` and `performance`.  A `show` is something like a movie, play, concert or wedding. Each `show` has a title and details plus at least one performance date/time.  Each of those date/time entries needs to have a corresponding `performance` as well, and each  `performance` content has specifics about that particluar instance of the `show`, things like:

  - the showFormat, be it '2D', '3D', or 'Not Applicable'
  - the assigned volunteer team,
    - the Manager, or 'TBD' if it is yet to-be-determined
    - the Monitor and M-Partner, or 'TBD' if they are yet to-be-determined
    - the Concessions and C-Partner, or 'TBD' if they are yet to-be-determined
    - the Ticket Seller, or 'TBD' if it is yet to-be-determined
  - any Notes that are specific to this `performance`

In my https://hikes.summittdweller.com site I publish a record of hikes and bike rides I have captured.  In that project folder there is a Python3 script named `generate-hikes.py` that I use to create new "hikes" content pages from captured .gpx files.  The script basically looks at all .gpx files in the project's `static/gpx` folders and checks the `content/hikes` folders for a corresponding .md file.  If no corresponding file exists, the script will rename the .gpx file per an established standard, and create a new .md file in `content/hikes`.

I envision having a similar script for this task, one that will look at all the .md files in `site/content/show`, parse all of the performance date/time values for each .md file, and determine if there's already a corresponding .md file in `site/content/performance`.  If there is, leave it be.  If there is not, a new file should be created and populated with pertinent information from the `show`, including a reference back to the `show`'s .md file.  _A copy of `generate-hikes.py` has been placed in the Wieting project folder and renamed `generate-performances.py`._
  
## Add Google, or Other, Calendar Page(s)

Several possibilities here...

https://gohugohq.com/partials/activity-calendar-posts/
https://yueyvettehao.netlify.app/post/2020-05-07-activitycalendar/
https://www.raymondcamden.com/2017/02/24/an-example-of-a-static-site-with-a-dynamic-calendar
https://discourse.gohugo.io/t/adding-public-google-calendar-into-hugo-site/31258

The Wieting already has a Google Calendar, but there's not a lot of data in it yet, at https://calendar.google.com/calendar/u/0/r.  

## Add Donor Recognition Text to the Home Page

Michelle tells me that recognition of the following is required in a prominent location on the site...

_Thank you to the: Iowa Department of Cultural Affairs, The Iowa Economic Development Authority, and Arts Midwest for your support which helped us to navigate thru a difficult year!_
 
 I may create a new "appreciation" block above the home page marquee to display this list.  Perhaps we can replace it in a few months, or when any new substantial donors are identifed?

## Add a Pop-Up Notification "Overlay" to the Home Page

_Digital.Grinnell_ now employs a _Drupal_ module that can provide a pop-up (Javascript driven) "overlay" message.  The message can be given and _expiryDate_ when it automatically disappers, and the user can easily click it out of the way once it's been read.  It would be nice to have the same for the Wieting.  Initial message might be that we plan to show "classic" movies on Sunday evening only until COVID-19 numbers decline more significantly.  

## Add Show URLs to Show's Page

There are two optional URLs for each Show, the "official" site and the IMDB page.  Please add display of both of these, if provided (don't print an empty label with no value), on each show's individual page.

## New "Camps" Page for Kids/Educational Events

Include .pdf forms for Summer camps like "All About the Arts" and "STEM Camp".

## Add a "Links" page with a list of external resources

Just what the heading implies.  Links can be found on a OneTab at https://www.one-tab.com/page/mb6s610ySvqnnQbwCi0_ZA.

## Add a "Network" page to document systems and connections

Just what the heading implies.  This page is available at https://wieting.tamatoledo.com/network. It includes a .png export of our latest networks diagram (still in progress).
