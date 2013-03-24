class Service
  include Mongoid::Document
  # field :name, type: String
  field :location, type: Array

  index({ location: "2d" }, { min: -180, max: 180 })
end