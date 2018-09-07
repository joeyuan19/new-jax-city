import re
import datetime
import urllib

URL_FORMATS = {
    'nydailynews.com':r'nydailynews.com/<FILLER><YEAR4><MONTH2><DAY2>',
    'streetsblog.org':r'streetsblog.org/<YEAR4>/<MONTH2>/<DAY2>',
    'nytimes.com':r'nytimes.com/<YEAR4>/<MONTH2>/<DAY2>',
    'nypost.com':r'nypost.com/<YEAR4>/<MONTH2>/<DAY2>',
}

REGEX_REPLACEMENTS = {
    '<FILLER>':'.*?',
    '<YEAR4>':'(?P<year>\d{4})',
    '<YEAR2>':'(?P<year>\d{4})',
    '<MONTH2>':'(?P<month>\d{2})',
    '<MONTH1>':'(?P<month>\d{1})',
    '<DAY2>':'(?P<day>\d{2})',
    '<DAY1>':'(?P<day>\d{1})',
}

def pad_year(year):
    if len(year) == 2:
        return '20'+year
    else:
        return year

def pad_zero(s):
    if len(s) == 1:
        return '0'+s
    return s 

for host in URL_FORMATS:
    for placeholder in REGEX_REPLACEMENTS:
        URL_FORMATS[host] = URL_FORMATS[host].replace(placeholder,REGEX_REPLACEMENTS[placeholder])

def load_urls(filename):
    urls = []
    with open(filename,'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                urls.append(line)
    return urls

def parse_url_date(url):
    for host,pattern in URL_FORMATS.items():
        if host in url:
            result = re.search(pattern,url)
            y = result.group('year')
            m = result.group('month')
            d = result.group('day')
            date = datetime.datetime(int(pad_year(y)),int(m),int(d))
    return date

def sort_by_date(urls):
    return sorted(urls,key=lambda x: parse_url_date(x))

def write_to_file(filename,urls):
    with open(filename,'w') as f:
        for url in urls:
            f.write(url+'\n')

if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) < 1:
        print 'file not provided'
        print 'proper use:'
        print 'python news_order_by_date.py my_list_of_links.txt'
        sys.exit()
    
    filename = args[0] 
    urls = load_urls(filename)
    
    for url in urls:
        with urllib.urlopen(url) as f:
            i = f.info()
            print i.keys()
            break


