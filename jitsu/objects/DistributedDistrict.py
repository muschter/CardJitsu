from direct.distributed.DistributedObject import DistributedObject


class DistributedDistrict(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.uberInterest = None
        self.population = 0

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.uberInterest = self.cr.addInterest(self.getDoId(), 2, 'uberZone', 'uberInterestComplete')

        self.acceptOnce('uberInterestComplete', self.cr.uberZoneInterestComplete)
        self.cr.districtObj = self

    def postGenerateMessage(self):
        messenger.send('gotDistrict')

    def delete(self):
        if self.uberInterest:
            self.cr.removeInterest(self.uberInterest, 'clearInterestDone')
            self.uberInterest = None

        self.cr.districtObj = None
        DistributedObject.delete(self)

    def setPopulation(self, population):
        self.population = population
        messenger.send('popChanged', [population])

    def getPopulation(self):
        return self.population
