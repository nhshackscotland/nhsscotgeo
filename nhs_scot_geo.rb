require_relative 'env'
require_relative 'models/service'
require 'json'

RADIUS_OF_EARTH_IN_MILES = 3959

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

    if params[:categories]
      searched_services = Service.in(category: params[:categories].split(','))
    else
      searched_services = Service
    end

    # and finally run our query
    searched_services = searched_services.
      geo_near(latlngs).
      spherical.
      distance_multiplier(RADIUS_OF_EARTH_IN_MILES).
      unique(true)

    searched_services.to_json
  end
end

get "/services/:id.json" do
  content_type :json
  # my kingdom for a 'blank' method!
  Service.find(params[:id]).to_json unless params[:id] == nil
end

def hopefully_helpful_example
  {
    :status => "bad request",
    :message => "Sorry, you'll need to send latitude and longitude with your requests for search to work. Try the example below:",
    :example => "http://domain.org/services/search/ll=55,55"
  }.to_json
end
