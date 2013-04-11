nhsscotgeo
==========

This is a service to provide information previously made available over NHS24, via an RESTful API, in json, that can be filtered by:

#### The kind of service it is

You can filter based on the service you need: do you need a GP? Pharmacy? Minor injuries unit? etc.)

#### Distance from your current location

All the services listed that have postcodes have been geo-encoded, which means that your query can only show services within *n* kilomters from you.


## How to run this yourself

##### Get the data

First you'll need the correct data to import. Once the licensing is clear, it'll be linked here somehow, otherwise, you'll need to send an email to the list below to have it shared with you via dropbox. Sorry about this faff.

Still with us?

##### Load your gems

This is a sinatra app, using Mongoid to speak to a mongodb server, so pull down your gems:

    bundle

##### Start mongodb

We're running a mongodb app, so we'll need a service running somewhere. Best to install mongodb the best way you feel comfortable doing so. This has been build on mongodb 2.2 so far.

##### Import the data

Assuming you have the data, you'd run a command a bit like this, to import the file from the csv file that woul d have been shared with you:

    mongoimport --db mongoid --collection services --type csv --headerline --file data/all_data.csv

##### Index and clean up the data

There are a couple of rake tasks to clean up the data and make sure there are indexes present:

    rake setup:fixed_phone_format
    rake setup:service_location_indexes

These should be called if you just run `rake`, but check the other tasks too  - they'll help when checking the data later.

##### Run it

Run your sinatra app which ever way you like:

    ruby nhs_scot_geo.rb

Or with rackup:

    rackup

Or, in development:

    shotgun

#### Questions?

If you have any issues, please email [little-sick-app@googlegroups.com](mailto:little-sick-app@googlegroups.com).
