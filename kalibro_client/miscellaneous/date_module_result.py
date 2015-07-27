from recordtype import recordtype

class DateModuleResult(recordtype('DateModuleResult',
                                  ('date', 'module_result'))):
    __slots__ = ()

    @property
    def result(self):
        return self.module_result.grade
