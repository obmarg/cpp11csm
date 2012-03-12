define [
  "Underscore",
], ( _ ) ->

  class CompilerVersion
    constructor: ( @Name, @ShortName, @Version, @AltVersion ) ->

  class App
    initialize: ->
      $( 'button.show-all' ).click( ->
        # show everything manually then change the checkboxes,
        # seems that the change event doesn't get sent when changing
        # things this way.  Probably faster doing it manually as well
        $( '[data-compilerid]' ).attr( 'data-hidden', false ).show()
        window.TheApp.checkHideOrShow()
        $( '.compilerCheckbox' ).children(
          'input:checkbox'
        ).prop( 'checked', true )
        return false
      )
      $( 'button.show-none' ).click( ->
        # Likewise here, hide everything manually
        $( '[data-compilerid]' ).attr( 'data-hidden', true ).hide()
        window.TheApp.checkHideOrShow()
        $( '.compilerCheckbox' ).children(
          'input:checkbox'
        ).prop( 'checked', false )
        return false
      )
      $( 'input:radio[name=displayAvaliable]' ).change( ->
        window.TheApp.checkSettings()
        window.TheApp.checkHideOrShow()
      )
      @doCheckHide = false
      $( ".compilerCheckbox" ).change(
        @checkCompilerSettings
      ).not( ':checked' ).each( @checkCompilerSettings )
      @doCheckHide = true
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

    checkCompilerSettings : ()->
        checkbox = $( this ).children().first()
        compilerId = checkbox.val()
        checked = checkbox.attr( 'checked' )
        window.TheApp.doCompilerCheck( compilerId, checked )

    doCompilerCheck: ( compilerId, checked ) ->
      # A handler for changing the compiler checkboxes
      # Params:
      # compilerId  - The id of the compiler
      # checked - Whether or not the checkbox is checked
      #
      targets = $( "[data-compilerid=" + compilerId + "]" )
      if checked
        targets.attr( 'data-hidden', 'false' ).show()
      else
        targets.attr( 'data-hidden', 'true' ).hide()
      if @doCheckHide
      	@checkHideOrShow()

    checkHideOrShow: ->
      if @displayOnlyAvaliable
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
          	me.show( )
          if not anySupported and me.is(':visible')
          	me.hide( 300 )
        )
      else
      	$("#coreLanguageBody").find("tr").show( 1000 )
 
  initialize = ->
    window.TheApp = new App
    window.TheApp.initialize()

  initialize: initialize
