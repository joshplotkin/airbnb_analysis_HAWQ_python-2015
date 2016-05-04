import numpy as np
import math
import json
import requests
import sys
import cPickle as pickle
import time 

class GetIDs:
	def __init__(self, repeats):
		''' repeats is the number of times to repeat search query.
		this is necessary due to inconsistent API search results. 
		-- self.all_ids is an array of IDs
		-- self.hood_counts is count of IDs by neighborhood'''
		self.repeats = repeats
		# TODO: just get a neighborhood list
		# and don't require an expected amount
		self.init_neighborhood_counts(15, 0)
		# print self.neighborhood_counts
		# change to all hoods
		self.get_all_listings()
		self.make_output_structures()

	def make_output_structures(self):
		ids = self.search_dict
		self.all_ids = []
		self.hood_counts = {}
		for hood in ids.keys():
		    self.hood_counts[hood] = 0
		    for rng in ids[hood].keys():
		        self.hood_counts[hood] += int(ids[hood][rng]['count'])
		        self.all_ids.append(ids[hood][rng]['ids'])
		self.all_ids = list(set(all_ids))


	def get_all_listings(self):
		self.search_dict = {}
		for h in sorted(self.neighborhood_counts.keys()):
			n = self.neighborhood_counts[h]
			# ensure that r reflects the count in neighborhood_counts
			self.search_dict[h] = {}
			# no results for this neighborhood
			if n == 0:
				self.search_dict[h][str([1,100000])] = {'count':0, 'ids':[]}
			# split
			# TODO: make split "durable"
			elif n > 1000:
				self.split_search(h, n, [1,100000])
			else:
				self.search_dict[h][str([1,100000])] = {'count':n, 'ids': self.get_all_ids([1,100000], h, n)}

	# queries the search API taking price and/or neighborhood (as list)
	def query_search_api(self, offset, min_price=None, max_price=None, hood_list=None):
		if hood_list:
			if type(hood_list) is str:
				hood_list = [hood_list]
			hoods = ''.join(['&neighborhoods%5B%5D=' + hood for hood in hood_list])
		url = 'https://api.airbnb.com/v2/search_results'
		url += '?client_id=3092nxybyb0otqw18e8nh5nty&locale=en-US'
		url += '&currency=USD&_format=for_search_results&_limit=50'
		url += '&_offset='  + str(offset)
		url += '&guests=1&ib=false&ib_add_photo_flow=true'
		url += '&location=New%20York%2C%20NY&min_bathrooms=0'
		if hood_list:
			url += hoods
		url += '&min_bedrooms=0&min_beds=0'
		if min_price:
			url += '&price_min=' + str(min_price) + '&price_max=' + str(max_price)
		url += '&min_num_pic_urls=10&mobile_session_id=&sort=1&suppress_facets=false'
		r = json.loads(requests.get(url).text.encode('utf-8'))
		
		# API rate limit exceeded -- pause <wait_mins> minutes
		wait_mins = 10
		while 'error_code' in r.keys() and r['error_code'] == 503:
			sys.stderr.write('API limit exceeded -- waiting ')
			for i in range(wait_mins):
				sys.stderr.write(str(wait_mins-i) + ' more minutes... ')
				time.sleep(60)
			r = json.loads(requests.get(url).text.encode('utf-8'))
			sys.stderr.write('\n')

		# other error codes, e.g. searched too far back
		if 'error_code' in r.keys():
			return None
		return r

	# extracts number of search hits for a given seach API JSON object	    
	def num_search_results(self, r):
		if r['metadata']['pagination']['result_count'] == 0:
			return 0

		return [c for c in r['metadata']['facets']['bedrooms'] \
		  if c['key'] == 0][0]['count']

	# try search API <repeats> times and find the most common result
	def init_neighborhood_counts(self, repeats, offset):
		dict_of_counts = {}
		for _ in range(repeats):
			r = self.query_search_api(0)
			for h in r['metadata']['facets']['neighborhood_facet']:
				hood = str(h['value'].encode('utf-8'))
				num = int(h['count'])

				if hood not in dict_of_counts.keys():
					dict_of_counts[hood] = np.array(num)
				else:
					dict_of_counts[hood] = np.append(dict_of_counts[hood], num)

			self.neighborhood_counts = { k:dict_of_counts[k].max() for k in dict_of_counts.keys() }

	# given a price range and neighborhood, extract all IDs
	# make sure we get n results (give or take 10% or 2 total results, whichever is more)
	def get_all_ids(self, price_range, neighborhood, expected_count):

		# extract all IDs from an API query
		def get_chunk_list(offset, price_range, neighborhood):
			r = self.query_search_api(offset, price_range[0], price_range[1], neighborhood)
			return self.extract_ids(r)

		all_ids = np.empty([0,0])
		for offset in range(0, 1050, 50):
			zero_repeats = 0
			# fifty = 0
			curr_ids = np.empty([0,0])

			# due to quirks in the search API, the results are inconsistent
			# and so by repeating the search, we can get a more consistent result
			for _ in range(self.repeats):
			# if we find 50 results, move to the next iteration

				# TODO: make get_chunk_list make np array; rename to arr
				chunk_id_list = np.array(get_chunk_list(offset, price_range, neighborhood))
				curr_ids = np.append(curr_ids, chunk_id_list)

				# if len(chunk_id_list) == 50:
				# 	fifty += 1
				# break if it gets 50- 5 times
				# if fifty == 5:
				# 	break

				if len(chunk_id_list) == 0:
					zero_repeats += 1
					# break if it gets 0- 5 straight times
					if zero_repeats == 5:
						break
				else:
					# if it's ever >0, it should never
					# have a chance of breaking early
					zero_repeats = -1000

			# print 'curr', curr_ids.shape[0], np.unique(curr_ids).shape[0]
			all_ids = np.append(all_ids, curr_ids)
			# print '    total', curr_ids.shape[0], np.unique(all_ids).shape[0]
			# save only unique values
			all_ids = np.unique(all_ids)

			# break if it gets 0- 5 straight times
			if zero_repeats == 5:
				break

		print 'finished ', neighborhood, price_range, ' expected ', expected_count, ' found ', all_ids.shape[0]
		return all_ids

	# extracts list of IDs from search API JSON object
	def extract_ids(self, r):
		if not r:
			return []
		ids = [i['listing']['id'] for i in r['search_results']]
		return ids

	# for searches over 1000 results, split it into parts by partitioning the
	# price range search space
	def split_search(self, neighborhood, num_results, price_range):
		init_lower = price_range[0]
		# cap the upper at 300 so the search range
		# doesn't put too much weight in high values
		init_upper = min(300, price_range[1])
		
		# split it in parts based on size of current search query
		splits = int(math.ceil(num_results/1000.))+1
		increment = int((init_upper-init_lower)/float(splits))

		lower = init_lower-1
		for i in range(splits):
			# last one, use upper bound as top and not 300
			if i == splits-1:
				upper = price_range[1]
			else:
				upper = lower + increment
				
			# try search here... if under 1000, keep it (base case)
			# else call recursive function again
			for _ in range(5):
				r = self.query_search_api(0, lower+1, upper, neighborhood)
				n = self.num_search_results(r)
				if n > 1000:
					break

			# base case: extract first page of IDs
			if n <= 1000:
				self.search_dict[neighborhood][str([lower+1,upper])] = \
				   {'ids':self.get_all_ids([lower+1,upper], neighborhood, n)}            
			# can't split anymore to get under 1000... unlikely to ever happen
			# if it does, just treat it as under 1000
			elif lower+1 >= upper:
				print 'too many results for neighborhood ' + h + ' and price ' + str(lower+1) + ',' + str(upper)
				self.search_dict[neighborhood][str([lower+1,upper])] = \
				   {'ids':self.get_all_ids([lower+1,upper], neighborhood, n)}            
			# split again
			else:
				self.split_search(neighborhood, n, [lower+1, upper])
			# for next iteration
			lower += increment

if __name__ == '__main__':
	ids = GetIDs(5)
	pickle.dump(ids, open('id_search_dict' + str(np.random.random()).split('.')[-1][:5] + '.pickle', 'wb'))