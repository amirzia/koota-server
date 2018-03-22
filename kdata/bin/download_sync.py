import argparse
import datetime
import glob
import json
import os
import subprocess
import sys
try:
    # python3
    import requests
    from urllib.request import Request, urlopen
    import urllib.parse as parse
except:
    from urllib2 import Request, urlopen
    import urllib2.parse as parse


parser = argparse.ArgumentParser(description="Koota data download")
parser.add_argument("base_url")
parser.add_argument("converter")
parser.add_argument("output_dir")
#parser.add_argument("--session-id")
#parser.add_argument("--device")
parser.add_argument("-f", "--format", default='sqlite3dump')
parser.add_argument("--out-db", default=None)
parser.add_argument("--group", default=None, action='store_true')

args = parser.parse_args()

baseurl = args.base_url
baseurl_p = parse.urlparse(args.base_url)

#class auth(requests.auth.AuthBase):
#    def __call__(self, r):
#        r.cookies = dict(sessionid=args['session_id'])
#        import IPython ; IPython.embed()
#        return r


def get(url, params={}):
    #R = Request(url, headers={'Cookie': 'sessionid='+os.environ['session_id']})

    r = requests.get(url, params=params, headers={'Cookie': 'sessionid='+os.environ['session_id']})
    if r.status_code != 200:
        print(url, params)
        raise Exception("requests failure: %s %s"%(r.status_code, r.reason))
    return r.text

format = args.format
today = datetime.date.today()

# Get data
if not args.group:
    R = get(os.path.join(baseurl, 'json'))
else:
    R = get(os.path.join(baseurl, args.converter, 'json'))
print(R)
data = json.loads(R)
if data['data_exists']:
    earliest_ts = data['data_earliest']
    latest_ts = data['data_latest']
    earliest = datetime.datetime.fromtimestamp(earliest_ts)
    latest = datetime.datetime.fromtimestamp(latest_ts)
    current_day = earliest.date()


    while current_day < latest.date():
        # process [current_date, current_date+1)
        current_day += datetime.timedelta(days=1)

        outfile = current_day.strftime(args.converter+'.%Y-%m-%d'+'.'+format)
        outfile = os.path.join(args.output_dir, outfile)
        if os.path.exists(outfile+'.partial'):
            os.unlink(outfile+'.partial')
        if current_day == today:
            outfile = outfile + '.partial'
        print(outfile, end='  ', flush=True)

        if os.path.exists(outfile):
            print()
            continue

        # download data
        R = get(os.path.join(baseurl, args.converter)+'.'+format,
                             params=dict(start=current_day.strftime('%Y-%m-%d'),
                                         end=(current_day+datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                                        ))
        print('%-7d'%len(R))
        open(outfile, 'w').write(R)

    if format == 'sqlite3dump':
        current_files = glob.glob(os.path.join(args.output_dir, args.converter+'.*.sqlite3dump'))
        current_files.sort()
        if args.out_db is None:
            dbfile = os.path.join(args.output_dir, 'db.sqlite3')
        else:
            dbfile = args.out_db
        if os.path.exists(dbfile):
            os.unlink(dbfile)

        # Import the database
        sql_proc = subprocess.Popen(['sqlite3', dbfile, '-batch'], stdin=subprocess.PIPE)
        sql_proc.stdin.write(b'.bail ON\n')
        #sql_proc.stdin.write(b'.echo ON\n')
        sql_proc.stdin.write(b'PRAGMA journal_mode = OFF;\n')
        sql_proc.stdin.write(b'PRAGMA synchronous = OFF;\n')
        for filename in current_files:
            cmd = '.read %s'%filename
            print(cmd)
            sql_proc.stdin.write(cmd.encode()+b'\n')
        sql_proc.stdin.write(b'PRAGMA synchronous = NORMAL;\n')
        sql_proc.stdin.close()
        sql_proc.wait()
