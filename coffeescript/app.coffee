define [
  "Mustache",
  "Underscore",
  "text!data/compilers.json",
  "text!data/languagefeatures.json",
  "text!templates/compilerSelection.html"
], ( Mustache, _, compilersJson, languageFeaturesJson, compilersTemplate ) ->

  class CompilerVersion
    constructor: (@Name, @ShortName, @Version, @AltVersion ) ->

  class App
    initialize: ->
      compilers = $.parseJSON( compilersJson )
     
      # TODO: Need to sanitise the version numbers somehow.
      #       They all contain _s, so can't be used for IDs as they
      #       are just now
      $( "#compilerVersions" ).html(
        Mustache.render( compilersTemplate, compilers )
      )
      changeHandler = ->
        @updateFeatureTable()
      changeHandler = _.bind( changeHandler, @ )
      $( ".compilerCheckbox" ).change( changeHandler )

      @compilers = compilers.compilers
      # Now, transform the input JSON into a nice array of 
      # [ CompilerVersion... ]
      # which should make it easier to deal with everything later
      @compVers = []
      names = _.pluck( @compilers, "Name" )
      shortNames = _.pluck( @compilers, "ShortName" )
      compVers = (
        _.zip(
          _.pluck( comp.Versions, "Num" ),
          _.pluck( comp.Versions, "AltNum" )
        ) for comp in @compilers
      )
      @appendVersions( nameVer ) for nameVer in _.zip( names, shortNames, compVers )

      @languageFeatures = $.parseJSON( languageFeaturesJson ).features

      @updateFeatureTable()

    appendVersions: ( nameVer ) ->
      # Takes an array of [ Name, ShortName [ [ VerNum, AltVer ]... ] ]
      # Should append to @compVers

      # TODO: It would be good if we maybe used objects
      #         rather than arrays for this
      @compVers.push(
        new CompilerVersion(
          nameVer[ 0 ], nameVer[ 1 ], verNum[0], verNum[ 1 ]
        )
      ) for verNum in nameVer[ 2 ]

    updateFeatureTable: ->
      # Updates the feature table with actual data
      @checkSettings()
      strArray = (
        compVer.Name + " " + compVer.Version for compVer in @activeCompilers
      )

      headerArray = ( "<th>#{str}</th>" for str in strArray )

      $( "#coreLanguageHeader" ).html(
        "<th>Feature</th>" + headerArray.join( "" )
      )

      featureArray = (
        @processFeature( feature ) for feature in @languageFeatures
      )

      $( "#coreLanguageBody" ).html(
        featureArray.join( "\n" )
      )

    compilerCheckboxActive: ( compVer ) ->
      # Checks if a compiler versions checkbox has been checked
      $( "#" + compVer.ShortName + compVer.AltVersion + "check:checked" ).length != 0

    checkSettings: ->
      # Checks the checkbox settings, and sets up data appropriately
      #
      # First, check what compilers we're using
      @activeCompilers = (
        cv for cv in @compVers when @compilerCheckboxActive( cv )
      )

    processFeature: (feature) ->
      # Processes a feature.  Returns the appropriate HTML row in string form
      name = feature.Name
      output = "<tr>\n<td>#{name}</td>\n"
      supportArray = (
        @featureSupported(
          compVer, feature.Support
        ) for compVer in @activeCompilers
      )
      rowArray = ( @getTableCell( supported ) for supported in supportArray )
      output + rowArray.join( "\n" ) + "</tr>"

    featureSupported: ( compVer, supportObj ) ->
      # Checks if a feature is supported on a particular compiler version
      # compVer : The compiler version
      # supportObj : An object { CompilerName : MinVersion }
      if supportObj[ compVer.Name ]?
      	supportedVer = parseFloat( supportObj[ compVer.Name ] )
      	actualVer = parseFloat( compVer.Version )
      	return actualVer >= supportedVer
      return false

    getTableCell : ( supported ) ->
      # Returns a <td> string for a table cell
      # supported : True if the feature is supported
      if supported
      	return "<td class='success'>Yes</td>"
      else
      	return "<td class='error'>No</td>"



  initialize = ->
    window.TheApp = new App
    window.TheApp.initialize()

  initialize: initialize
