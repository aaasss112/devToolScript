class NullPointException(Exception):
    def __init__(self, field=None, msg=None):
        self.field = field
        self.msg = msg

    def __str__(self):
        print("the field [%s] is Null, msg = %s" % (self.field, self.msg))
