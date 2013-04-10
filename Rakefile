require_relative 'env'
require_relative 'models/service'
require 'dotenv/tasks'

namespace :setup do

  desc "Add the location array for the services collection to geosearch"
  task :service_location_indexes do

    Service.each do |s|
      s.location = [s.longitude.to_f, s.latitude.to_f]
      s.save
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

desc "Import mongodb codes. Do not run on production"
task :import => :dotenv do
  puts "mongoimport -h #{ENV['LITTLESICK_HOSTNAME']} -d #{ENV['LITTLESICK_DATABASE']} -c services -u #{ENV['LITTLESICK_USER']} -p #{ENV['LITTLESICK_PASSWORD']} --file data/all_data.csv --type csv --headerline"
end

desc "Clear existing database, ready for new import"
task :destroy_everything do
  Service.destroy_all
end
