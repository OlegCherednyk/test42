
class Frange:
    class FrangeIter:
        def __init__(self, lim1, lim2, step):
            self._step = step
            self._lim1 = lim1
            self._lim2 = lim2
            self._pointer = 0

        def __next__(self):
            if self._pointer > abs((self._lim2 - self._lim1)/self._step):
                raise StopIteration
            if self._pointer == 0:
                result = self._lim1
            else:
                result = self._lim1 + self._step
                self._lim1 = result
            self._pointer += 1

            return result

    def __init__(self, lim2, lim1=0, step=1):
        self._step = step

        if lim1 == 0:
            self._lim1 = lim1
            self._lim2 = lim2
        else:
            self._lim1 = lim2
            self._lim2 = lim1

    def __iter__(self):
        return self.FrangeIter(self._lim1, self._lim2, self._step)


f = Frange(0, -5, -0.5)
frange = iter(f)

print(f._lim1)
print(f._lim2)

print('-----------')

print(next(frange))
print(next(frange))
print(next(frange))
print(next(frange))
