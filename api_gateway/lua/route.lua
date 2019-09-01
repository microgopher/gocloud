-- curl --header "Content-Type: application/json" --header "X-API-KEY: c43433e972"   --request POST   --data '{"username":"xyz1","password":"xyz1"}'   http://localhost:8080/api/auth/register
local redis = require 'resty.redis'
local http = require "resty.http"
local cjson = require "cjson.safe" 
local red = redis:new()
local ok, err = red:connect(os.getenv("REDIS_HOST"), 6379)
if not ok then 
    ngx.say(cjson.encode({status="ok", errormessage=
        "Failed to connect to the redis server the error was: "..err})) 
    ngx.exit(500) 
end 
function string:split(delimiter)
    local result = { }
    local from  = 1
    local delim_from, delim_to = string.find( self, delimiter, from  )
    while delim_from do
      table.insert( result, string.sub( self, from , delim_from-1 ) )
      from  = delim_to + 1
      delim_from, delim_to = string.find( self, delimiter, from  )
    end
    table.insert( result, string.sub( self, from  ) )
    return result
end

local keys = string.split(ngx.var.uri, "/")
local url = "/"..keys[2].."/"..keys[3]
local apiroute = red:get("api:"..url)

if apiroute == ngx.null then 
    ngx.say(cjson.encode({status="error", errormessage=
           "no service at this path"})) 
    ngx.exit(404) 
end 
local route = apiroute
if (keys[4])
then
    route = route.."/"..keys[4] 
end
local headers = ngx.req.get_headers()
local req_method = ngx.req.get_method()
local method = ngx.HTTP_POST
if (req_method == "POST")
then
    method = ngx.HTTP_POST
elseif (req_method == "HEAD")
then
    method = ngx.HTTP_HEAD
elseif (req_method == "PUT")
then
    method = ngx.HTTP_PUT
elseif (req_method == "GET")
then
    method = ngx.HTTP_GET
elseif (req_method == "DELETE")
then
    method = ngx.HTTP_DELETE
end

ngx.req.read_body()
local body = ngx.req.get_body_data()

res = ngx.location.capture("/proxy/"..route, {
    method = method,
    body = body
}) 
if res then 
    ngx.say(cjson.encode({status=res.status, result=res.body, header=res.header})) 
else 
    ngx.say(cjson.encode({status="error",
           errormessage="service failed to return a result"})) 
    ngx.exit(500) 
end

-- local res, err = httpc:request_uri("http://"..route, {
--     method = method,
--     body = body,
--     headers = headers,
--     keepalive_timeout = 60,
--     keepalive_pool = 10
-- })

-- if not res then
--     ngx.say("failed to request: ", err)
--     ngx.exit(500) 
--     return
-- end

-- -- -- for k,v in pairs(res.headers) do
-- -- --     --
-- -- -- end

-- ngx.status = res.status
-- ngx.say(res.body)




