define [
  "Underscore",
], ( _ ) ->

  class CompilerVersion
    constructor: ( @Name, @ShortName, @Version, @AltVersion ) ->

  class App
    initialize: ->
      # TODO: delete this next block of code (replace it with a different handler)
      $( ".compilerCheckbox" ).change( ->
        checkbox = $( this ).children().first()
        compilerId = checkbox.val()
        checked = checkbox.attr( 'checked' )
        window.TheApp.checkCompilerSettings( compilerId, checked )
        window.TheApp.checkHideOrShow()
      )
      $( 'input:radio[name=displayAvaliable]' ).change( ->
        window.TheApp.checkSettings()
        window.TheApp.checkHideOrShow()
      )
      @checkSettings()
      @checkHideOrShow()
      
    checkSettings: ->
      # Checks the checkbox settings, and sets up data appropriately
      #
      # First, check what compilers we're using
      if $('input:radio[name=displayAvaliable]:checked').val() == "yes"
      	@displayOnlyAvaliable = true
      else
      	@displayOnlyAvaliable = false

    checkCompilerSettings: ( compilerId, checked ) ->
      # A handler for changing the compiler checkboxes
      targets = $( "[data-compilerid=" + compilerId + "]" )
      if checked
        targets.show( 1000 )
        targets.attr( 'data-hidden', 'false' )
      else
        targets.hide( 1000 )
        targets.attr( 'data-hidden', 'true' )


    checkHideOrShow: ->
      # Using globals in here, to save on having to bind
      # the function to this properly
      if window.TheApp.displayOnlyAvaliable
        # TODO: Hide shit
        $("#coreLanguageBody").find("tr").each( ->
          anySupported = false
          me = $(this)
          me.find( "td" ).each( ->
            if $(this).attr( 'data-supported' ) == 'true'
              if $(this).attr( 'data-hidden' ) == 'false'
                anySupported = true
          )
          if anySupported and not me.is(':visible')
          	me.show( 1000 )
          if not anySupported and me.is(':visible')
          	me.hide( 1000 )
        )
      else
      	$("#coreLanguageBody").find("tr").show( 1000 )
 
  initialize = ->
    window.TheApp = new App
    window.TheApp.initialize()

  initialize: initialize
