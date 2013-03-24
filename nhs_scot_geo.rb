require_relative 'env'
require_relative 'models/service'
require 'json'

get "/services/search.json" do
  if params['ll'].nil?
    content_type :json

    # send a bad request 400 along, but give clues how to use the API
    [400, hopefully_helpful_example]
  else
    content_type :json

    # naively assuming our lat-longs will only ever look like 57,44
    latlngs = params['ll'].split(',')

    # we need to make sure we pass numbers into our query or Mongoid complains
    latlngs.map! { |l| l.to_f }

    # and finally run our query
    searched_services = Service.geo_near(latlngs).spherical.unique(true)

    searched_services.to_json
  end
end

def hopefully_helpful_example
  {
    :status => "bad request",
    :message => "Sorry, you'll need to send latitude and longitude with your requests for search to work. Try the example below:",
    :example => "http://domain.org/services/search/ll=55,55"
  }.to_json
end
