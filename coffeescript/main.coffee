require.config
  paths:
    Mustache: "libs/mustache/mustache-wrapper"
  #baseUrl: "/static/"

require [ "app" ], (App) ->
  App.initialize()
