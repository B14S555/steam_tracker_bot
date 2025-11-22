app = "steam-tracker-bot"

[build]
  image = "python:3.11-slim"

[env]
  PORT = "8080"
  FLY_APP_HOST = "https://steam-tracker-bot.fly.dev"

[[services]]
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    port = 80
