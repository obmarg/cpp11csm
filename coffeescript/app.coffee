define [
  "libs/mustache/mustache-wrapper",
  "text!data/compilers.json",
  "text!data/languagefeatures.json"
], ( Mustache, compilers, languageFeatures ) ->

  initialize = ->
    alert( "initialised" );

  initialize: initialize
