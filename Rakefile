require_relative 'env'
require_relative 'models/service'

desc "Add the location array for the services collection to geosearch"
task :add_locations do
  Service.each do |s|
    s.location = [s.longitude, s.latitude]
    s.save
    puts "#{s.name}"
    puts "#{s.location}"
  end
end