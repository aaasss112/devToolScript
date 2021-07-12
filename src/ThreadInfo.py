class ThreadInfo:

    def __init__(self, name, count):
        self.count = count
        self.name = name

    def plusCount(self):
        self.count = self.count + 1

    def __str__(self):
        return "(%s,%s)" % (self.name, self.count)
