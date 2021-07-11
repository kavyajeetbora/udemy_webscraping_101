function main(splash, args)
  headers = {
    ["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
  }
  splash:set_custom_headers(headers)


  -- set private mode to false
  splash.private_mode_enabled = false

  -- set images loading to false to improve processing
  splash.images_enabled = false


  --[[
  When setting the images to false, this might load the images as well
  This is because the images are already cached by the browser when loading
  for the first time.

  Solution:
  To restart the splash engine again in docker

  ]]--

  assert(splash:go(args.url))
  splash:wait(1)

  return {
    png = splash:png(),
    html = splash:html()
  }
end
