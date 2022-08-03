class Lexicon(object):

    def __init__(self):
        self.directions = ['north', 'south', 'east', 'west', 'down', 'up', 'left', 'right', 'back']
        self.verbs = ['go', 'stop', 'kill', 'eat']

    def scan(self, str):
        words = self.split(str)
        results = []
        for word in words:
            if word in self.directions:
                results.append(('direction', word))
            elif word in self.verbs:
                results.append(('verb', word))
            else:
                results.append(('error', word))

        return results


    def convert_number(str):
        try:
            return int(str)
        except ValueError:
            return None

    def split(self, str):
        return str.split(" ")