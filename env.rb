require 'pry'
require 'sinatra'

require 'mongoid'


if ENV['RACK_ENV'] == 'development'

  require 'dotenv'
  Dotenv.load
end

Mongoid.logger.level = Logger::DEBUG
Moped.logger.level = Logger::DEBUG

puts ENV['MONGOLAB_URI']
Mongoid.load!("mongoid.yml", ENV['RACK_ENV'])

