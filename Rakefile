require_relative 'env'
require_relative 'models/service'

desc "Add the location array for the services collection to geosearch"
task :add_locations do

  Service.each do |s|
    s.location = [s.longitude.to_f, s.latitude.to_f]
    s.save
    # puts s.location
  end
end

desc "Drop into a REPL"
task :pry do
  binding.pry
end
