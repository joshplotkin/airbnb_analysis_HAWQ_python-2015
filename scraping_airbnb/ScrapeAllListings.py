import math
import json
import requests
import operator

def search_range_json(r, page = 1):
    url = 'https://www.airbnb.com/search/search_results'
    url += '?page=' + str(page)
    url += '&location=New+York%2C+NY%2C+United+States&price_min=' 
    url += str(r[0]) + '&price_max=' + str(r[1])
    return json.loads(requests.get(url).text)

def make_ranges_from_hist(hist):
    minm = 0
    curr = None
    ranges = []
    tot = 0
    for h in hist:
        # no previous one, and current one > 300
        if tot == 0 and h[0] > 300:
            ranges.append([minm, h[1], h[0]])
            minm = h[1] + 1
        # there is a previous, and current > 300
        elif h[0] > 300:
            ranges.append([minm, curr, tot])
            ranges.append([curr+1, h[1], h[0]])
            tot = 0        
            minm = h[1] + 1
            curr = h[1]
        # if this one puts it over 300
        elif tot + h[0] > 300:
            ranges.append([minm, curr, tot])
            tot = 0        
            minm = h[1] + 1
            curr = h[1]
        else:
            tot += h[0]
            curr = h[1]
    #     ranges.append([curr, float('inf'), h[0]])
    return ranges


def convert_count(c):
    if c == '300+':
        return 999
    else:
        return int(c)


def breakdown_range(r, return_range, increment_size, listing_dict):
    ## make sure increment size at least cuts it in half
    increment_size = min(round((r[1]-r[0])/2.,0), increment_size)
    increment_size = max(1, increment_size)

    # recursively break ranges
    # base cases: min and max are 0 or 1 apart
    if r[0] == r[1]:
        data = search_range_json([r[0],r[0]])
        count = data['results_count_string']\
                     .split(' ')[0]
        for listing in data['logging_info']['pricing'].keys():
            listing_dict[listing] = {'page':1}
        return_range.append([int(r[0]), int(r[0]), convert_count(count)])
                
    # if total <= 300, return them together
    # else separately
    elif r[1] - r[0] == 1:
        tmp = []
        for i in [0, 1]:
            data = search_range_json([r[i],r[i]])
            count = data['results_count_string']\
                         .split(' ')[0]
            for listing in data['logging_info']['pricing'].keys():
                # if already in dict
                if listing in listing_dict.keys():
                    print 'listing already in dict'
                    print r, listing_dict[listing]
                listing_dict[listing] = {'page':1, 'search_range':[r[0], r[1]]}
                
            tmp.append([int(r[i]), int(r[i]), convert_count(count)])
        # can fit
        if sum([tmp[i][2] for i in [0,1]]) > 300:
            return_range.append(tmp[0])
            return_range.append(tmp[1])
        else:
            return_range.append([r[0], r[1], sum([tmp[i][2] for i in [0,1]])])
            for listing in data['logging_info']['pricing'].keys():
                # if already in dict
                if listing in listing_dict.keys():
                    print 'listing already in dict'
                    print r, listing_dict[listing]
                listing_dict[listing] = {'page':1, 'search_range':[r[0], r[1]]}
            
            return [return_range, listing_dict]

    else:
        # make a list of proposed ranges
        # TODO:
        # values ending in 00 or 99 have lots of listings
        proposed = []
        # subtract 1 to handle overlap
        lower = r[0]-1
        while lower < r[1]:
            upper = min(lower+increment_size, r[1])
            # add 1 to prevent overlap
            proposed.append([lower+1, upper, None])
            lower = upper

        for curr_rng in proposed:

            data = search_range_json(curr_rng)

            # under 300
            if data['results_count_string'].split(' ')[0] != '300+':
                curr_rng[2] = int(data['results_count_string'].split(' ')[0])
                for listing in data['logging_info']['pricing'].keys():
                    listing_dict[listing] = {'page':1}
                    
                return_range.append(curr_rng)
            
            elif data['results_count_string'].split(' ')[0] == '300+':
                # still 300+ ... break down further
                return_range, listing_dict = breakdown_range([curr_rng[0], curr_rng[1]], \
                                               return_range, int(increment_size/2.), \
                                              listing_dict)
            else:
                print 'bug; shouldnt be here'
                sys.exit(0)


    return [return_range, listing_dict]

def neighborhood_list(neighborhoods):
    full_string = ''
    base = '&neighborhoods%5B%5D='
    for n in neighborhoods:
        full_string += base + n
    return full_string

def search_range_json(r, page = 1, neighborhoods = None, br = None, bed = None, bath = None):
    url = 'https://www.airbnb.com/search/search_results'
    url += '?page=' + str(page)
    url += '&location=New+York%2C+NY%2C+United+States'
    url += '&price_min=' + str(r[0]) + '&price_max=' + str(r[1])
    if neighborhoods:
        url += neighborhood_list(neighborhoods)
    if br:
        url += '&min_bedrooms=' + str(br)
    if bed:
        url += '&min_bathrooms=' + str(bath)
    if bath:
        url += '&min_beds=' + str(bed)
    r = requests.get(url).text
    if '<title>503 Service Unavailable - Airbnb</title>' in r:
        print 'RECEIVED 503 SERVICE UNAVAILABLE ERROR'
        sys.exit(0)
    print url
    return json.loads(r)


def create_neighborhood_lists(hoods):
    # request didn't work
    if 'facet-count' not in hoods['filters']:
        return None
    
    boroughs = ['Manhattan','Bronx','Brooklyn','Queens','Staten Island']
    neighborhoods = {}
    started = False
    for d in [d.strip() for d in hoods['filters'].split('\n') if d.strip() != '']:
        if started == True:
            if 'facet-count' in d:
                neighborhoods[curr] = convert_count(d.split('(')[1].split(')')[0])
                started = False
        elif '<input type="checkbox" name="neighborhood"' in d:
            curr = d.split('value="')[1].replace('">','').replace(' ','+')
            if curr not in boroughs:
                started = True
                
        
    # TODO: sort dictionary alphabetically, or do list of tuples

    tot = 0
    lists = []
    curr_list = []
    for k in neighborhoods.keys():
        if tot + neighborhoods[k] > 275:
            lists.append(curr_list)
            curr_list = [k]
            tot = 0 
        else:
            curr_list.append(k)
            tot += neighborhoods[k]
    lists.append(curr_list)
    
    return lists    

# get an estimate of the ranges from the histogram
data = search_range_json([0, 5000])

histtmp = data['logging_info']['search']['result']['resultSetSummary']
hist = zip(histtmp['priceHistogramCounts'], histtmp['priceHistogramPrices'])
est_ranges = make_ranges_from_hist(hist)


final_ranges = []
for r in est_ranges:
    data = search_range_json(r)
    if data['results_count_string'].split(' ')[0] == '300+':
        breakdown, listing_dict = breakdown_range(r, [], 8, {})
        final_ranges.extend(breakdown)
    else:
        r[2] = int(data['results_count_string'].split(' ')[0])
        final_ranges.append(r)

under300 = [f for f in final_ranges if f[2] < 999]
over300 = [f for f in final_ranges if f[2] == 999]

over300_with_neighborhoods = []

for o in over300:
    # keep trying request until it is successful
    data = search_range_json([55, 55], 1, None, 1, 1, 1)
    while 'facet-count' not in data['filters']:
        data = search_range_json([55, 55], 1, None, 1, 1, 1)

    neighborhood_lists = create_neighborhood_lists(data)
    
    # print out number of hits
    for i in neighborhood_lists:
        data = search_range_json([o[0], o[1]], 1, i, 1, 1, 1)
#         print o, data['results_count_string'].split(' ')[0]
        
        r = [o[0], o[1], data['results_count_string'].split(' ')[0], i]
        over300_with_neighborhoods.append(r)
    
        for listing in data['logging_info']['pricing'].keys():
            # if already in dict
#             if listing in listing_dict.keys():
#                 print 'listing already in dict'
#                 print listing_dict[listing]
            listing_dict[listing] = {'page':1, 'search_range':r}        