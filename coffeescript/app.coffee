define [
  "Mustache",
  "Underscore",
  "text!data/compilers.json",
  "text!data/languagefeatures.json",
  "text!templates/compilerSelection.html"
], ( Mustache, _, compilersJson, languageFeaturesJson, compilersTemplate ) ->

  class App
    initialize : ->
      compilers = $.parseJSON( compilersJson )
      
      $( "#compilerVersions" ).html(
        Mustache.render( compilersTemplate, compilers )
      )

      @compilers = compilers.compilers
      # Now, transform the input JSON into a nice array of 
      # [ [ CompilerName, Version ]... ]
      # which should make it easier to deal with everything later
      @compVers = []
      names = _.pluck( @compilers, "Name" )
      compVers = ( _.pluck( comp.Versions, "Num" ) for comp in @compilers )
      @appendVersions( nameVer ) for nameVer in _.zip( names, compVers )

    appendVersions : ( nameVer ) ->
      # Takes an array of [ Name, [ VerNum... ] ]
      # Should append to @compVers
      @compVers.push( [ nameVer[ 0 ], verNum ] ) for verNum in nameVer[ 1 ]

    checkSettings : ->
      # Checks the checkbox settings, and sets up data appropriately
      #
      # First, check what compilers we're using
      @activeCompilers = [] 

    useVersion : ( name, num ) ->
      # Checks if a version has been selected by the user

    updateFeatureTable : ->
      # Updates the feature table with actual data
      strArray = ( compVer[0] + " " + compVer[1] for compVer in @compVers )

      headerArray = ( "<th>#{str}</th>" for str in strArray )

      $( "#coreLanguageHeader" ).html(
        "<th>Feature</th>" + headerArray.join( "" )
      )


  initialize = ->
    window.TheApp = new App
    window.TheApp.initialize()

  initialize: initialize
