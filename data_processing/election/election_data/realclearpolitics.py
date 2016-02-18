from bs4 import BeautifulSoup
import requests
import os
from datetime import date

class poll_scraper():
	def __init__(self, year):
		self.year = year
		self.curr_year = True
		
	def source(self,url,path = None):
		if not path:
			resp = requests.get(url)
			return resp.text
		else:
			return open(path).read()

	def clean_date(self,row):
		if not row:
			return None
		raw_date = row[1]
		raw_spl = raw_date.split('-')
		if not raw_spl[0]:
			return ''
		month = int(raw_spl[0].split('/')[0])
		
		if self.curr_year or month < 4:
			year = self.year
			if month < 4:
				self.curr_year = False
		else:
			year = self.year - 1
			
		days = (int(raw_spl[0].split('/')[1]),int(raw_spl[1].split('/')[1]))
		day = (days[0]+days[1])/2
		if (date(self.year,11,1) - date(year,month,day)).days > 365:
			return False
		return '-'.join([str(year),str(month),str(day)])
		
	def scrape(self,path_out,url):
		soup = BeautifulSoup(self.source(url),"html.parser")
		headers = []
		out = open(path_out,'w')
		clean_date = ''
	# 	urllib2: "class = 'data large '"
		
		table = soup.find_all('table',{'class':'data'})
		if len(table) == 1:
			table = table[0]
		else:
			table = table[1]
		
		for th in table.find_all('th'):
			headers.append(str(th.get_text().encode('ascii','ignore').strip()))
		out.write('|'.join(headers) + '\n')
		
		for tr in table.find_all('tr'):
			row = []
			for td in tr.find_all('td'):
				row.append(str(td.get_text()).strip())
			if row:
				clean_date = self.clean_date(row)
				if clean_date == False:
					break
				row[1] = clean_date
				out.write('|'.join(row) + '\n')
			if clean_date == False:
				break
		out.close()
		
		self.curr_year = True
		del soup
	
def gen_election_scrape():

	def run(year, url,state = ""):
		dir = "/Users/HANK/Documents/data_processing/election/election_data/{year}_election"
		base_out = '{state}poll_presidential_general_election_{year}.txt'
		path = os.path.join(dir.format(year = str(year)),base_out.format(state = state + '_', year = str(year)))
		ps = poll_scraper(year)
		ps.scrape(path,url)

# 	year = 2004
# 	url = "http://www.realclearpolitics.com/epolls/2004/president/us/general_election_bush_vs_kerry-939.html"
# 	run(year,url)
# 	
# 	year = 2008
# 	url = "http://www.realclearpolitics.com/epolls/2008/president/us/general_election_mccain_vs_obama-225.html"
# 	run(year,url)
# 	
# 	year = 2012
# 	url = "http://www.realclearpolitics.com/epolls/2012/president/us/general_election_romney_vs_obama-1171.html"
# 	run(year,url)
# 	
# 	year = 2016
# 	gop_url = "http://www.realclearpolitics.com/epolls/2016/president/nh/new_hampshire_republican_presidential_primary-3350.html"
# 	dem_url = "http://www.realclearpolitics.com/epolls/2016/president/nh/new_hampshire_democratic_presidential_primary-3351.html"
# 	run(year,gop_url)
# 	run(year,dem_url)
	
	year = 2016
	gop_url = "http://www.realclearpolitics.com/epolls/2016/president/sc/south_carolina_republican_presidential_primary-4151.html"
	dem_url = "http://www.realclearpolitics.com/epolls/2016/president/nv/nevada_democratic_presidential_caucus-5337.html"
	run(year,gop_url,state = 'gop_SC')
	run(year,dem_url,state = 'dem_NV')

def polls_by_state():
	
	def run(get_states, year, url, race_type):
		print year
		dir = "election/election_data/{year}_election"
		base_out = 'state_poll_presidential_general_election_{year}.txt'
		path = os.path.join(dir.format(year = str(year)),base_out.format(year = str(year)))
		ps = poll_scraper(year)
		ps.get_polls_by_state(get_states, url, race_type)
		del ps
	
# 	files
# def get_links(path):
# 	links = open(path).read()
# 	return links.replace('\r','\n').split('\n')
# 	
# def file_run():
# 	years = {2012:["president","senate"],2014: ["governor","senate"]}
# 	presidential
# 	
# 	# path to links
# 	base_dir = 	"""
# 				/Users/HANK/Documents/data_processing/election/election_data/
# 				{year}_election/{type}_poll_links_by_state.txt
# 				"""
# 	# where we will send results
# 	path_out = 	"""
# 				/Users/HANK/Documents/data_processing/election/election_data/
# 				{year}_election/{state}_{type}_election_{year}.txt
# 				"""
# 	
# # 	cycle through files, scrape all links
# 	for year in years:
# 		types = years[year]
# 		for type in types:
# 			links = open(base_dir.format(year = str(year), type = type)).read()
# 			links = links.replace('\r','\n').split('\n')
# 			if not ("http" == links[0][0:5]):
# # 				some links are missing the first half
# 				for link in links:
# 					os.path.join("http://www.realclearpolitics.com/",link)
# 			
# 			for link in links
# 					path = path_out.format(year = str(year), state = link[-2], type = type)
# 					ps = poll_scraper(url,year)
# 					ps.scrape(path,url)
# 		
# 	files = get_links(path

if __name__ == '__main__':
	gen_election_scrape()
	# polls_by_state()

	