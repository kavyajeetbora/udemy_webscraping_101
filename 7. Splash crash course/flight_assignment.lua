function main(splash, args)

  -- set custom headers
  headers = {
    ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    --["Accept-Language"] = "en-US,en;q=0.9,fr-DZ;q=0.8,fr;q=0.7,ar;q=0.6"
    ['Cookie'] = 'w_locale=fr_DZ'
  }
  splash:set_custom_headers(headers)

  -- request the homepage of the website
  assert(splash:go(args.url))

  return {
    png = splash:png(),
    history = splash:history()
  }
end
