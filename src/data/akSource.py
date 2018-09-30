from src.data.akEnums import AkSourceType


class AkSource(object):
    """
    The sources of the section for the Analysis.
    The structure_type of the object:
    dict {AkSectionType: list[AkPeriod()]; AkSectionType: list[AkPeriod()]}
    """
    def __init__(self):
        self._source = {
            AkSourceType.D.name: [],
            AkSourceType.W.name: [],
            AkSourceType.M.name: [],
            AkSourceType.Q.name: [],
            AkSourceType.Y.name: []
        }

    def addSource(self, xPeriod, sectionType=None):
        """
        Add sources to the sources object.
        :param xPeriod: Object of AkPeriod() class.
        """
        if (sectionType is not None):
            type = sectionType
        else:
            type = xPeriod.dataType()

        values = self.getPeriodValues(type)

        if (xPeriod.number() not in values):
            self._source[type.name].append(xPeriod)

    def getPeriodValues(self, sectionType):
        periods = self.getSource(sectionType)
        periodValues = []
        for period in periods:
            periodValues.append(period.value())

        return periodValues

    def sections(self):
        """
        Get sources sections list.
        :return: List[] of section names.
        """
        return self._source.keys()

    def getSource(self, sectionType):
        """
        Get initial period of the section.
        :param section: AkSourceSection enumeration.
        :return: list[AkPeriod()]
        """
        return self._source[sectionType]