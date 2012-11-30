from EntityUtil import Cleaner
from Rule import Rule

class RuleSet():
    def __init__(self, selector, values, comment, styleSheet):
        self.extra = False
        self.roughSelector = selector
        self.roughValue = values
        self.roughComment = comment

        self.selector = Cleaner.clearSelector(selector)
        self.values = Cleaner.clearValues(values)
        self.comment = Cleaner.clearComment(comment)

        self.fixedSelector = ''
        self.fixedComment = ''

        self.styleSheet = styleSheet
        self._rules = []

        self.singleLineFlag = (len(self.roughValue.split('\n')) == 1)

    def extendSelector(self, other):
        self.roughSelector = self.roughSelector + ',' + other.roughSelector
        self.selector = self.selector + ',' + other.selector
        self.fixedSelector = self.fixedSelector + ',' + other.fixedSelector

        if len(other.comment) != 0 and self.comment.find(other.comment) == -1:
            # do not need duplicated comment
            self.roughComment = self.roughComment + ('\n' + other.roughComment)
            self.comment = self.comment + '\n' + other.comment
            self.fixedComment = self.fixedComment + '\n' + other.fixedComment

    def compressRules(self):
        collector = []
        for rule in self._rules:
            collector.append(rule.compress())
        collected = ''.join(collector)
        if collected != '':
            collected = collected[0:-1]
        return collected

    def compress(self):
        result = self.selector if self.fixedSelector == '' else self.fixedSelector
        if result.find(','):
            # remove duplicated selectors
            selectors = []
            for x in result.split(','):
                x = x.strip()
                if x in selectors:
                    continue
                selectors.append(x)
            result = ','.join(selectors)
        result = result + '{' + self.compressRules() + '}'
        return result

    def fixedRules(self):
        collector = []
        spaces = ' ' * 4
        for rule in self._rules:
            collector.append(spaces + rule.fixed())
        collected = '\n'.join(collector)
        return collected

    def fixed(self):
        result = self.comment if self.fixedComment == '' else self.fixedComment
        result = result + '\n' + (self.selector if self.fixedSelector == '' else self.fixedSelector)
        if result.find(','):
            # remove duplicated selectors
            selectors = []
            for x in result.split(','):
                x = x.strip()
                if x in selectors:
                    continue
                selectors.append(x)
            result = ',\n'.join(selectors)
        result = result + ' {\n' + self.fixedRules() + '\n}'
        return result

    def getSingleLineFlag(self):
        return self.singleLineFlag

    def getStyleSheet(self):
        return self.styleSheet

    def addRuleByStr(self, selector, attr, value):
        self._rules.append(Rule(selector, attr, value, self))

    def indexOf(self, name):
        counter = 0
        for rule in self._rules:
            if rule.roughName.strip() == name:
                return counter
            counter = counter + 1
        return -1
    
    def removeRuleByIndex(self, index):
        if index < len(self._rules):
            self._rules[index] = None

    def clean(self):
        newRules = []
        for rule in self._rules:
            if rule is None:
                continue
            newRules.append(rule)
        self._rules = newRules

    def existNames(self, name):
        if name.find(',') != -1:
            names = name.split(',')
        else:
            names = [name]
        for name in names:
            name = name.strip()
            for rule in self._rules:
                if rule.name == name:
                    return True
        return False

    def existRoughNames(self, name):
        if name.find(',') != -1:
            names = name.split(',')
        else:
            names = [name]
        for name in names:
            name = name.strip()
            for rule in self._rules:
                if rule.roughName.strip() == name:
                    return True
        return False

    def getRuleByStrippedName(self, name):
        for rule in self._rules:
            if rule.strippedName == name:
                return rule

    def getRuleByRoughName(self, name):
        for rule in self._rules:
            if rule.roughName == name:
                return rule

    def getRuleByName(self, name):
        for rule in self._rules:
            if rule.name == name:
                return rule

    def getRules(self):
        return self._rules

    def setRules(self, newRules):
        self._rules = newRules

    def __str__(self):
        return '%s {%s}' % (self.selector, self.roughValue)
