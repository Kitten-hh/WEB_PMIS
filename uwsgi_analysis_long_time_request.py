logfile = 'uwsgi.log'
import re

with open(logfile, 'r') as file:
    regex = r"in (\d+) msecs"
    url_regex = r"(GET|POST|PUT|DELETE|PATCH)\s(\/[^?\s]+)"
    urls = {}
    for line in file:
        match = re.search(regex, line)
        if match:
            processing_time = float(match.group(1))
            if processing_time >= 2000:
                url_match = re.search(url_regex, line)
                if url_match:
                    url = url_match.group(2)
                    if url not in urls:
                        urls[url] = {"time":processing_time, "line":line}
    urls = dict(sorted(urls.items(), key=lambda x:x[1]['time'], reverse=True))
    for url in urls.values():
        print(url['line'])