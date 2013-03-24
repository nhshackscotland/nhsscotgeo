class Service
  include Mongoid::Document
  field :location, type: Array

  index({ location: "2d" }, { min: -180, max: 180 })
end