
class Sdict(dict):

    def  add(self,request,spider):
        _ = spider.name
        if _ in self:
            self[_].add(request)
        else:
            self[_] = set()
            self[_].add(request)

    def get(self, k):
        v = sorted(self[k],key=lambda req:-req.priority)
        return v

#
# a = Sdict()
# a.add(type('r',(),{'priority':12})(),type('dd',(),{'name':'lo'})())
# a.add(type('r',(),{'priority':2})(),type('dd',(),{'name':'lo'})())
# a.add(type('r',(),{'priority':82})(),type('dd',(),{'name':'lo'})())
# a.add(type('r',(),{'priority':0})(),type('dd',(),{'name':'lo'})())
#
# for i in a.get('lo'):
#     print(i.priority)
#
# c = a.pop('lo')
# print(c)
# print(';',a)
