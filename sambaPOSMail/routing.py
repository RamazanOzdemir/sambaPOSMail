from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    print('******************') 
    # Empty for now (http->django views is added by default)
})
