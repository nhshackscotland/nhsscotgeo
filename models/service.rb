class Service
  include Mongoid::Document
  field :location, type: Array

  index({ location: "2d" }, { min: -90, max: 90 })
end