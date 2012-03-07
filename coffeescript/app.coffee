define [
  "Underscore",
], ( _ ) ->

  class CompilerVersion
    constructor: (@Name, @ShortName, @Version, @AltVersion ) ->

  class App
    initialize: ->
      # TODO: delete this next block of code (replace it with a different handler)
      $( ".compilerCheckbox" ).change( ->
        # A handler for changing the compiler checkboxes
        checkbox = $( this ).children().first()
        compilerId = checkbox.val()
        targets = $( "[data-compilerid=" + compilerId + "]" )
        if checkbox.attr( 'checked' )
          targets.show( 1000 )
        else
          targets.hide( 1000 )
        )

    checkSettings: ->
      # Checks the checkbox settings, and sets up data appropriately
      #
      # First, check what compilers we're using
      if $('input:radio[name=displayAvaliable]:checked').val() == "yes"
      	@displayOnlyAvaliable = true
      else
      	@displayOnlyAvaliable = false

  initialize = ->
    window.TheApp = new App
    window.TheApp.initialize()

  initialize: initialize
