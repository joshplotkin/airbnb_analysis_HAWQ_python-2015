CREATE DATABASE airbnb;
\c airbnb

CREATE EXTERNAL TABLE ext_listings(
   lid TEXT
  , access TEXT
  , address TEXT
  , amenities TEXT
  , bathrooms TEXT
  , bed_type TEXT
  , bed_type_category TEXT
  , bedrooms TEXT
  , beds TEXT
  , calendar_updated_at TEXT
  , cancel_policy TEXT
  , cancel_policy_short_str TEXT
  , cancellation_policy TEXT
  , check_in_time TEXT
  , check_out_time TEXT
  , city TEXT
  , cleaning_fee_native TEXT
  , description TEXT
  , extra_user_info TEXT
  , extras_price_native TEXT
  , guests_included TEXT
  , has_agreed_to_legal_terms TEXT
  , has_availability TEXT
  , has_double_blind_reviews TEXT
  , has_viewed_terms TEXT
  , house_rules TEXT
  , instant_bookable TEXT
  , interaction TEXT
  , is_location_exact TEXT
  , lat TEXT
  , license TEXT
  , listing_cleaning_fee_native TEXT
  , listing_price_for_extra_person_native TEXT
  , listing_security_deposit_native TEXT
  , listing_weekend_price_native TEXT
  , lng TEXT
  , max_nights_input_value TEXT
  , min_nights_input_value TEXT
  , monthly_price_factor TEXT
  , monthly_price_native TEXT
  , name TEXT
  , neighborhood TEXT
  , neighborhood_overview TEXT
  , notes TEXT
  , person_capacity TEXT
  , picture_count TEXT
  , price TEXT
  , price_for_extra_person_native TEXT
  , property_type TEXT
  , require_guest_profile_picture TEXT
  , review_rating_accuracy TEXT
  , review_rating_checkin TEXT
  , review_rating_cleanliness TEXT
  , review_rating_communication TEXT
  , review_rating_location TEXT
  , review_rating_value TEXT
  , reviews_count TEXT
  , room_type TEXT
  , room_type_category TEXT
  , security_deposit_native TEXT
  , security_price_native TEXT
  , smart_location TEXT
  , space TEXT
  , special_offer TEXT
  , square_feet TEXT
  , star_rating TEXT
  , summary TEXT
  , transit TEXT
  , user_id TEXT
  , weekly_price_factor TEXT
  , weekly_price_native TEXT
  , zipcode TEXT
) LOCATION ('pxf://localhost:50070/airbnb/listings.csv?profile=HdfsTextSimple')
FORMAT 'CSV'  (HEADER DELIMITER  as '|') LOG ERRORS INTO errors SEGMENT REJECT LIMIT 1000;

CREATE TABLE listings(
   lid INT
  , access TEXT
  , address TEXT
  , amenities TEXT
  , bathrooms FLOAT
  , bed_type TEXT
  , bed_type_category TEXT
  , bedrooms INT
  , beds INT
  , calendar_updated_at TEXT
  , cancel_policy INT
  , cancel_policy_short_str TEXT
  , cancellation_policy TEXT
  , check_in_time INT
  , check_out_time INT
  , city TEXT
  , cleaning_fee_native INT
  , description TEXT
  , extra_user_info TEXT
  , extras_price_native INT
  , guests_included INT
  , has_agreed_to_legal_terms BOOLEAN
  , has_availability BOOLEAN
  , has_double_blind_reviews TEXT
  , has_viewed_terms BOOLEAN
  , house_rules TEXT
  , instant_bookable BOOLEAN
  , interaction TEXT
  , is_location_exact BOOLEAN
  , lat FLOAT
  , license TEXT
  , listing_cleaning_fee_native INT
  , listing_price_for_extra_person_native INT
  , listing_security_deposit_native INT
  , listing_weekend_price_native INT
  , lng FLOAT
  , max_nights_input_value INT
  , min_nights_input_value INT
  , monthly_price_factor FLOAT
  , monthly_price_native TEXT
  , name TEXT
  , neighborhood TEXT
  , neighborhood_overview TEXT
  , notes TEXT
  , person_capacity INT
  , picture_count INT
  , price INT
  , price_for_extra_person_native INT
  , property_type TEXT
  , require_guest_profile_picture BOOLEAN
  , review_rating_accuracy INT
  , review_rating_checkin INT
  , review_rating_cleanliness INT
  , review_rating_communication INT
  , review_rating_location INT
  , review_rating_value INT
  , reviews_count INT
  , room_type TEXT
  , room_type_category TEXT
  , security_deposit_native INT
  , security_price_native INT
  , smart_location TEXT
  , space TEXT
  , special_offer TEXT
  , square_feet INT
  , star_rating FLOAT
  , summary TEXT
  , transit TEXT
  , user_id INT
  , weekly_price_factor FLOAT
  , weekly_price_native INT
  , zipcode TEXT
) with (APPENDONLY=true, orientation=parquet) 
DISTRIBUTED randomly;

INSERT INTO listings 
SELECT 
 lid::INT
, access::TEXT
, address::TEXT
, amenities::TEXT
, bathrooms::FLOAT
, bed_type::TEXT
, bed_type_category::TEXT
, bedrooms::INT
, beds::INT
, calendar_updated_at::TEXT
, cancel_policy::INT
, cancel_policy_short_str::TEXT
, cancellation_policy::TEXT
, check_in_time::INT
, check_out_time::INT
, city::TEXT
, cleaning_fee_native::INT
, description::TEXT
, extra_user_info::TEXT
, extras_price_native::INT
, guests_included::INT
, has_agreed_to_legal_terms::INT::BOOLEAN
, has_availability::INT::BOOLEAN
, has_double_blind_reviews::TEXT
, has_viewed_terms::INT::BOOLEAN
, house_rules::TEXT
, instant_bookable::INT::BOOLEAN
, interaction::TEXT
, is_location_exact::INT::BOOLEAN
, lat::FLOAT
, license::TEXT
, listing_cleaning_fee_native::INT
, listing_price_for_extra_person_native::INT
, listing_security_deposit_native::INT
, listing_weekend_price_native::INT
, lng::FLOAT
, max_nights_input_value::INT
, min_nights_input_value::INT
, monthly_price_factor::FLOAT
, monthly_price_native::TEXT
, name::TEXT
, neighborhood::TEXT
, neighborhood_overview::TEXT
, notes::TEXT
, person_capacity::INT
, picture_count::INT
, price::INT
, price_for_extra_person_native::INT
, property_type::TEXT
, require_guest_profile_picture::INT::BOOLEAN
, review_rating_accuracy::INT
, review_rating_checkin::INT
, review_rating_cleanliness::INT
, review_rating_communication::INT
, review_rating_location::INT
, review_rating_value::INT
, reviews_count::INT
, room_type::TEXT
, room_type_category::TEXT
, security_deposit_native::INT
, security_price_native::INT
, smart_location::TEXT
, space::TEXT
, special_offer::TEXT
, square_feet::INT
, star_rating::FLOAT
, summary::TEXT
, transit::TEXT
, user_id::INT
, weekly_price_factor::FLOAT
, weekly_price_native::INT
, zipcode::TEXT
 FROM ext_listings;

