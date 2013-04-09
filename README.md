nhsscotgeo
==========

Backend data to host geo location data for use within NHS Hack Scotland apps.

mongoimport --db mongoid --collection services --type csv --headerline --file data/all_data.csv

Example import for production

mongoimport -h ENV['LITTLESICK_HOSTNAME'] -d ENV['LITTLESICK_DATABASE'] -c services -u ENV[LITTLESICK_USER] -p ENV['LITTLESICK_PASSWORD'] --file data/all_data.csv --type csv --headerline

http://docs.mongodb.org/manual/reference/mongoimport/