require_relative 'env'
require_relative 'models/service'


namespace :nhs_scot_geo do

  task :add_locations
    Service.each do |s|
      # puts s.longitude
      puts s.latitude

      s.location = [s.longitude, s.latitude]
      s.save
      puts "#{s.location}"
  end
end