import logging
from datamodel.search.datamodel import ProducedLink, OneUnProcessedGroup, robot_manager, Link
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter
import re, os
from time import time
from lxml import html
import requests

try:
    # For python 2
    from urlparse import urlparse, parse_qs
except ImportError:
    # For python 3
    from urllib.parse import urlparse, parse_qs

visited=set();
bad_urls=set();
logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"
url_count = (set() 
    if not os.path.exists("successful_urls.txt") else 
    set([line.strip() for line in open("successful_urls.txt").readlines() if line.strip() != ""]))
MAX_LINKS_TO_DOWNLOAD = 3000

@Producer(ProducedLink, Link)
@GetterSetter(OneUnProcessedGroup)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        # Set app_id <student_id1>_<student_id2>...
        self.app_id = "43351454_72114439_49699153"
        # Set user agent string to IR W17 UnderGrad <student_id1>, <student_id2> ...
        # If Graduate studetn, change the UnderGrad part to Grad.
        self.UserAgentString = "IR S17 43351454 72114439 49699153"
		
        self.frame = frame
        assert(self.UserAgentString != None)
        assert(self.app_id != "")
        if len(url_count) >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True
   


    def initialize(self):
        self.count = 0
        l = ProducedLink("http://www.ics.uci.edu", self.UserAgentString)
        print l.full_url
        self.frame.add(l)

    def update(self):
        for g in self.frame.get_new(OneUnProcessedGroup):
            print "Got a Group"
            outputLinks, urlResps = process_url_group(g, self.UserAgentString)
            for urlResp in urlResps:
                if urlResp.bad_url and self.UserAgentString not in set(urlResp.dataframe_obj.bad_url):
                    urlResp.dataframe_obj.bad_url += [self.UserAgentString]
            for l in outputLinks:
                if is_valid(l) and robot_manager.Allowed(l, self.UserAgentString):
                    lObj = ProducedLink(l, self.UserAgentString)
                    self.frame.add(lObj)
        if len(url_count) >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True

    def shutdown(self):
        print "downloaded ", len(url_count), " in ", time() - self.starttime, " seconds."
        pass

def save_count(urls):
    global url_count
    urls = set(urls).difference(url_count)
    url_count.update(urls)
    if len(urls):
        with open("successful_urls.txt", "a") as surls:
            surls.write(("\n".join(urls) + "\n").encode("utf-8"))

def process_url_group(group, useragentstr):
    rawDatas, successfull_urls = group.download(useragentstr, is_valid)
    save_count(successfull_urls)
    return extract_next_links(rawDatas), rawDatas
    
#######################################################################################
'''
STUB FUNCTIONS TO BE FILLED OUT BY THE STUDENT.
'''
def extract_next_links(rawDatas):
    outputLinks = list()
    for response in rawDatas:
        #check HTTP code 400+
        if(int(response.http_code) >=400):
        	response.bad_url = True;
        else:
            tree = html.fromstring(response.content);
            outputLinks.extend(tree.xpath("//a/@href"));
            #we visited the page and extracted all the links so add them to the visited
            #check if response is redirected then add the final url to the visited set
            if(response.is_redirected):
                visited.add(response.final_url);
            else:
                visited.add(response.url);
        
    '''
    rawDatas is a list of objs -> [raw_content_obj1, raw_content_obj2, ....]
    Each obj is of type UrlResponse  declared at L28-42 datamodel/search/datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.

    Suggested library: lxml
    '''
    return outputLinks





def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be downloaded or not.
    Robot rules and duplication rules are checked separately.

    This is a great place to filter out crawler traps.
    '''

    #function is used to check whether the url should be scraped
    #filter out the different type crawler traps
    #kill nested extreme directories traps

    if(url in visited):
    	print "URL-{} already visited".format(url);
    	return False;
   	if(url in bad_urls):
   		print "URL-{} is banned".format(url);
   		return False;
    if(re.match("^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", url)):
    	bad_urls.add(url);
        print "KILLED A REPEAT DIR TRAP-{}".format(url); 
        return False;
    #kill extra directories traps
    if(re.match("^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$" ,url)):
    	bad_urls.add(url);
        print "KILLED EXTRA DIRECTORY TRAPS-{}".format(url);
        return False;  
    # kill long messy wix urls
    if(re.match("^.*/[^/]{300,}$", url)):
    	bad_urls.add(url);
        print "KILLED LONG MESSY WIX URLS-{}".format(url);
        return False;      
    #kill calenders traps
    if(re.match("^.*calendar.*$", url)):
    	bad_urls.add(url);
        print "KILLED CALENDAR TRAP-{} ".format(url);
        return False;    
    
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
    	bad_urls.add(url);
        return False
    try:
        http_code = requests.get(url).status_code
        if(http_code >= 400):
            # print "code: {} KILLED BAD URL {}\n".format(http_code, url)
            bad_urls.add(url);
            return False;
    except requests.exceptions.ChunkedEncodingError as e:
        return False;

    try:
        visited.add(url)
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
