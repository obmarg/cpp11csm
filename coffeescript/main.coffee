require.config
  paths:
    Mustache: "libs/mustache/mustache-wrapper"
    Underscore: "libs/underscore/underscore-wrapper"
  #baseUrl: "/static/"

require [ "app" ], (App) ->
  App.initialize()
