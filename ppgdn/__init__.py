"""The Pirate Party Global Domain Network."""

# from understory import kv
# from understory import sql
from understory import web
# from understory.web.framework.util import tx


app = web.application("ppgdn", static=__name__, sessions=True)
tmpl = web.templates(__name__)


@app.route(r"")
class Home:
    """."""

    def _get(self):
        network = ["https://angelogladding.com"]
        return tmpl.home(network)


app.mount(web.cache_app)
app.mount(web.indieauth.client)
app.mount(web.indieauth.root)
app.mount(web.webmention.receiver)
app.mount(web.websub.hub)


@app.wrap
def contextualize(handler, app):
    """Contextualize this thread based upon the host of the request."""
    # host = tx.request.uri.host
    # tx.app.name = host
    # db = sql.db(f"{host}.db")
    # db.define(signins="""initiated DATETIME NOT NULL
    #                          DEFAULT CURRENT_TIMESTAMP,
    #                      user_agent TEXT, ip TEXT""",
    #           credentials="""created DATETIME NOT NULL
    #                              DEFAULT CURRENT_TIMESTAMP,
    #                          salt BLOB, scrypt_hash BLOB""",
    #           sessions=web.session_table_sql)
    # web.add_job_tables(db)
    # tx.host.db = db
    # tx.host.cache = web.cache(db=db)
    # tx.host.kv = kv.db(host, ":", {"jobs": "list"})
    yield


app.wrap(web.resume_session)
app.wrap(web.braidify)


# XXX @app.wrap
# XXX def template(handler, app):
# XXX     """Wrap the response in a template."""
# XXX     yield
# XXX     if tx.response.headers.content_type == "text/html" \
# XXX        and not tx.response.naked:
# XXX         tx.response.body = tmpl.template(tx.owner, tx.response.body)


app.wrap(web.indieauth.wrap_client, "post")
app.wrap(web.indieauth.wrap_server, "post")
app.wrap(web.micropub.wrap_server, "post")
app.wrap(web.microsub.wrap_server, "post")
app.wrap(web.webmention.wrap, "post")
app.wrap(web.websub.wrap, "post")
