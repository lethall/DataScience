import sqlite3
from random import choice
from bottle import get, run, response
from PIL import Image
from io import BytesIO

def get_id(id):
  db = sqlite3.connect(dn)
  d = db.execute("select d from im where id = ?", (id,)).fetchone()[0]
  db.close()
  return d

def yr(yy):
	return ['%d%02d' % (yy,m) for m in range(1,13)]

def cc(ar):
  ii = choice(ar)
  print(ii)
  return ii

fav = [9712,9511,8903,8406,8207,8112,7102,7009,7001,6906,6703,8310,7406]
dn = 
db = sqlite3.connect(dn)
a = [ii[0] for ii in db.execute("select id from im").fetchall()]
db.close()

ah = []
av = []
for ii in a:
  im = Image.open(BytesIO(get_id(ii)))
  if im.size[0] > im.size[1]:
    ah.append(ii)
  else:
    av.append(ii)

ayr = []
cyr = 70

@get('/id/<ii>')
def id(ii):
  response.set_header("Content-Type", "image/jpeg")
  return get_id(ii)

@get('/yr')
@get('/yr/<yy>')
def year(yy=70):
  global ayr, cyr
  response.set_header("Content-Type", "image/jpeg")
  if yy != cyr or len(ayr) == 0:
    ayr = yr(int(yy))
    cyr = yy
  return get_id(ayr.pop(0))

@get("/fv")
def fv():
  response.set_header("Content-Type", "image/jpeg")
  return get_id(cc(fav))

@get("/a")
def all():
  response.set_header("Content-Type", "image/jpeg")
  return get_id(cc(a))

@get("/h")
def h():
  response.set_header("Content-Type", "image/jpeg")
  return get_id(cc(ah))

@get("/v")
def v():
  response.set_header("Content-Type", "image/jpeg")
  return get_id(cc(av))

timer_script = '''
let timer;

function refreshOnInterval() {
    clearTimeout(timer);
    let ms, rt, attr;
    if (window.innerWidth > window.innerHeight) {
        ms = 10000;
        rt = "/h";
        attr = "width";

    } else {
        ms = 3000;
        rt = "/v";
        attr = "height";
    }
    const im = document.getElementById("im");
    im.setAttribute("src", rt);
    im.setAttribute(attr, "100%");
    timer = setTimeout(() => {
        location.reload();
        refreshOnInterval();
    }, ms);
}

refreshOnInterval();
window.addEventListener('resize', refreshOnInterval);
'''

@get("/ss")
def ss():
    return """<html>
    <body>
        <img id="im" >
        <script>""" + timer_script + """</script>
    </body></html>"""

@get("/ssa")
def ssa():
    return """<html>
    <body>
        <img id="im" src="/a">
        <script>
let timer;
const im = document.getElementById("im");

im.onload = function() {
	console.log("size " + im.naturalWidth + " x " + im.naturalHeight);
	if (im.naturalWidth > im.naturalHeight) {
	  im.style.width = '100%';
	  im.style.height = 'auto';
	} else {
		im.style.width = 'auto';
	  im.style.height = '100%';
	}
};

function refreshOnInterval() {
    clearTimeout(timer);
    timer = setTimeout(() => {
        location.reload();
        refreshOnInterval();
    }, 5000);
}

refreshOnInterval();
window.addEventListener('resize', refreshOnInterval);
        </script>
    </body></html>"""

run(host='0.0.0.0', port=8080, debug=True)
