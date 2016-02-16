from pyramid.request import Request

class MyRequest(Request):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ist.model.base import db
        db.connect()
        self.add_finished_callback(self.finish)

    def finish(self, request):
        from ist.model.base import db
        db.close()

