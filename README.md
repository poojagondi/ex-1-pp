# ex-1-pp
Setup ubuntu multipass with two machines, one nginx another is mysql. The nginx should reply pong when hit with port:80/ping. Along with this, record the number of hits coming to /ping in the database in a table. Taking a look at the mysql database should show how many hits have happened so far. Also log the source IP of the /ping requestor on the database
#what-i-did two ubuntu multipass vm- one for nginx+flask app and the other with mysql
 VM1- has nginx which listens on port 80(default for http requests)- this forwards incoming requests to "/ping" to the flask app running on the same vm but on port 5000. The flask app handles the /ping endpoint,records the number of hits in the mysql db and replies with "pong" on the ui. it also obtains the real ip of the client by trusting the "X-forwarded-For" header set by nginx using the ProxyFix middleware.
 VM2- has the mysql db which has a table used for tracking the number of hits to the url and the client ip.
#basic-workflow
1. Client sends the http req: browser/client hits http://<vm_ip>/ping on port 80.
2. nginx recieves the request, and proxies it internally to the flask app running on port 5000
3. nginx adds the x-forwarded-for header which gets client ip before forwarding the request
4. flask processes the request- flask basically recieves the proxied request using proxyfix middleware it extracts the real client ip from x-forwarded-for in request.remote_addr
5. flask connects to mysql vm- updates the db on the sql vm- increases the hit count, stores the client ip
6. flask returns the string pong to the http response to nginx.
