from pyramid.request import Request


def finish(request):
    from ist.model.base import db
    db.close()


class MyRequest(Request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ist.model.base import db
        db.connect()
        self.add_finished_callback(finish)

