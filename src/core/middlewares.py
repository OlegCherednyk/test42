import time


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        currtime = time.time()
        response = get_response(request)
        print("Time to function : %f" % (time.time() - currtime))
        return response

    return middleware
