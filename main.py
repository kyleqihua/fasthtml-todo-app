# type: ignore 
from fasthtml.common import *

app, rt = fast_app(live=True)

@rt("/")
def get():
    nums = NumList(8)
    return Titled("live homepage", Div(nums, id="staff", hx_get="/change"))

def NumList(i):
    return Ul(*[Li(o) for o in range(i)])

@rt("/change")
def get():
    return P("change can be good!")


serve() 