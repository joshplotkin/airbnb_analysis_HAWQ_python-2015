import requests
import json
import sys
import time

class ListingData:
    def __init__(self, lid):
        self.lid = lid
        self.listing = {}
        self.photos = {}
        self.extract_fact_data()

    # queries the search API taking price and/or neighborhood (as list)
    def query_api(self):
        url = 'https://api.airbnb.com/v2/listings/'
        url +=  str(self.lid) 
        url += '?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3'

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
            sys.stderr.write(str(self.lid))
            sys.stderr.write(str(r))
            sys.stderr.write('\n')
            return None

        return r

    def extract_fact_data(self):
        listing_attrs = [
        'cancel_policy_short_str','require_guest_profile_picture','property_type','security_deposit_native',
        'price_for_extra_person_native','monthly_price_native','has_double_blind_reviews','bedrooms','name',
        'notes','summary','special_offer','has_viewed_terms','has_agreed_to_legal_terms','neighborhood','lng',
        'neighborhood_overview','space','access','room_type_category','address','cleaning_fee_native',
        'square_feet','check_out_time','listing_security_deposit_native','license','guests_included',
        'reviews_count','transit','calendar_updated_at','review_rating_accuracy','extra_user_info','city',
        'user_id','review_rating_value','bed_type_category','person_capacity','extras_price_native',
        'instant_bookable','listing_cleaning_fee_native','interaction','picture_count','star_rating',
        'security_price_native','weekly_price_native','weekly_price_native','min_nights_input_value',
        'max_nights_input_value','bathrooms','cancellation_policy','check_in_time','is_location_exact',
        'zipcode','cancel_policy','house_rules','description','price','smart_location','lat','bed_type',
        'listing_price_for_extra_person_native','listing_weekend_price_native','beds','has_availability',
        'review_rating_communication','room_type','review_rating_cleanliness','review_rating_checkin',
        'review_rating_location','monthly_price_factor','weekly_price_factor']

        data = self.query_api()
        if data:
            self.listing = { k:data['listing'][k] for k in listing_attrs }
            self.listing['amenities'] = ','.join([str(l) for l in data['listing']['amenities']])

            photos_data = ['caption','picture','sort_order']
            for photo in data['listing']['photos']:
                self.photos[photo['id']] = { k:photo[k] for k in photos_data }
                self.photos[photo['id']]['lid'] = self.lid
        else:
            self.listing = None
            self.photos = None

# if __name__ == '__main__':
#   lid = '9805563'
#   ld = ListingData(lid)
#   print ld.listing
#   print ld.photos
#   print ld.data['listing']['user_id']
