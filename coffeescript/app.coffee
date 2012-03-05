define [
  "Mustache",
  "Underscore",
  "text!data/compilers.json",
  "text!data/languagefeatures.json",
  "text!templates/compilerSelection.html"
], ( Mustache, _, compilersJson, languageFeaturesJson, compilersTemplate ) ->

  class App
    initialize: ->
      compilers = $.parseJSON( compilersJson )
     
      # TODO: Need to sanitise the version numbers somehow.
      #       They all contain _s, so can't be used for IDs as they
      #       are just now
      $( "#compilerVersions" ).html(
        Mustache.render( compilersTemplate, compilers )
      )

      @compilers = compilers.compilers
      # Now, transform the input JSON into a nice array of 
      # [ [ CompilerName, ShortName, Version ]... ]
      # which should make it easier to deal with everything later
      @compVers = []
      names = _.pluck( @compilers, "Name" )
      shortNames = _.pluck( @compilers, "ShortName" )
      compVers = ( _.pluck( comp.Versions, "Num" ) for comp in @compilers )
      @appendVersions( nameVer ) for nameVer in _.zip( names, shortNames, compVers )
      @updateFeatureTable()

    appendVersions: ( nameVer ) ->
      # Takes an array of [ Name, [ VerNum... ] ]
      # Should append to @compVers

      # TODO: It would be good if we maybe used objects
      #         rather than arrays for this
      @compVers.push(
        [ nameVer[ 0 ], nameVer[ 1 ], verNum ]
      ) for verNum in nameVer[ 2 ]

    compilerCheckboxActive: ( compVer ) ->
      # Checks if a compiler versions checkbox has been checked
      $( "#" + compVer[1] + compVer[2] + ":checked" ).length != 0

    checkSettings: ->
      # Checks the checkbox settings, and sets up data appropriately
      #
      # First, check what compilers we're using
      @activeCompilers = (
        cv for cv in @compVers when @compilerCheckboxActive( cv )
      )

    useVersion: ( name, num ) ->
      # Checks if a version has been selected by the user

    updateFeatureTable: ->
      # Updates the feature table with actual data
      @checkSettings()
      strArray = ( compVer[0] + " " + compVer[2] for compVer in @activeCompilers )

      headerArray = ( "<th>#{str}</th>" for str in strArray )

      $( "#coreLanguageHeader" ).html(
        "<th>Feature</th>" + headerArray.join( "" )
      )


  initialize = ->
    window.TheApp = new App
    window.TheApp.initialize()

  initialize: initialize
