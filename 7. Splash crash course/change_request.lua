function main(splash, args)

  -- There are many options to set the headers:
  --[[
  -- Option 1: set custom user agent
  splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

  -- Option 2: set custom headers
  headers = {
    ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }
  splash:set_custom_headers(headers)
  ]]--

  -- Option 3: Using a call back function on request:
  splash:on_request(function(request)
    request:set_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
  end)

  --go the url
  assert(splash:go(args.url))

  --wait for the url to load the page for 1 second
  assert(splash:wait(1))

  --select the input box using css selector
  input = assert(splash:select("input[name='q']"))
  input:focus()

  -- Type the query to be searched for
  input:send_text("My User agent")

  --[[
  -- send the request using enter button
  input:send_keys("<Enter>")

  ]]

  -- There is another way: by selecting the button and using mouse click

  -- Select the button first and call the mouse click action
  button = splash:select_all("input[name='btnK']")
  assert(button[2].mouse_click())

  assert(splash:wait(1))

  return {
    png = splash:png(),
    html = splash:html(),
    -- Using history, we can take a look at the headers sent with the request
    history = splash:history()
  }
end
