function main(splash, args)
	assert(splash:go(args.url))
  assert(splash:wait(1))
  input = assert(splash:select("input[name='q']"))
  input:focus()
  input:send_text("My user agent")
  input:send_keys('<Enter>')
  assert(splash:wait(1))
  return {
    png = splash:png(),
    html = splash.html()
  }
end
