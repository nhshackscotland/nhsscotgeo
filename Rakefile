require_relative 'env'
require_relative 'models/service'

namespace :setup do

desc "Add the location array for the services collection to geosearch"
task :service_location_indexes do

  Service.each do |s|
    s.location = [s.longitude.to_f, s.latitude.to_f]
    s.save
    # puts s.location
  end

  Service.create_indexes

end

desc "format phone numbers as strings"
task :fixed_phone_format do
  count = 0
  Service.each do |s|

  if s.phone.class == Fixnum
      s.phone = "0#{s.phone}"
      s.save!
      count += 1
  end

  end
  puts count
end


end

desc "Drop into a REPL"
task :pry do
  binding.pry
end

task :default => ['setup:fixed_phone_format', 'setup:service_location_indexes']
