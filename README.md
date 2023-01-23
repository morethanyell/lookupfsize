# Lookup Table CSV File Size 
(I know. Annoyingly poor name of a Splunk app.)
### Just a custom Splunk command that retrieves a few details from CSV files and returns them with the event stream.
by morethanyell (daniel.l.astillero@gmail.com) <--- accepts beer
## Usage
### To use this command in just for ad hoc and you know the exact file path of your CSV lookup file, see below.

```
| makeresults 
| eval the_worlde_csv = "/opt/splunk/etc/apps/search/lookups/wordle.csv" 
| lookupfsize file_path=the_worlde_csv
```
What above does is simply getting the `file_size` of the CSV that's specified in the field. Below is an example of a use case that may be of value:
```
| rest /servicesNS/-/-/data/lookup-table-files 
| rename eai:data as path
| stats values(eai:acl.owner) as owner by path 
| lookupfsize file_path="path" verbose=1 prefix="csv_"
| sort 10 - csv_file_size
| convert ctime(csv_file_lastmod) timeformat="%F %X %Z"
```
Above simply gets the Top 10 largest CSV in your environment. Also, since sample SPL enables the paramater verbose, it also appends few more fields: the last modification date, the number of rows, and the number of columns.
## Installation
- Step 1: Download the Splunk app
    - Option 1: Splunkbase. Download the app from Splunkbase https://classic.splunkbase.splunk.com/app/6735/
    - Option 2: Github. Download the app from Github https://github.com/morethanyell/lookupfsize
- Step 2: Ensure the permission and ownership of the entirety of the app / directory `lookupfsize`
    - E.g.: `$ [sudo] chown -R splunk:splunk $SPLUNK_HOME/etc/apps/lookupfsize/`
    - Or whatever user is preferred over `splunk:splunk`
- Step 3: Restart your Splunk instance
    - E.g.: `$ ~/bin/splunk restart`

##### Buy me a bear: paypal.me/morethanyell