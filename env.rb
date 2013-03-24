require 'pry'
require 'sinatra'
require 'dotenv'
require 'mongoid'

Dotenv.load

Mongoid.logger.level = Logger::DEBUG
Moped.logger.level = Logger::DEBUG

Mongoid.load!("mongoid.yml", ENV['RACK_ENV'])

