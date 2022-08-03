from mystuff import apple, tangerine

apple()

print(tangerine)

class MyStuff(object):
    def __init__(self):
        self.name = "I'm V"
    def apple(self):
        print("I AM APPLES!")

thing = MyStuff()
thing.apple()
print(thing.name)


class Song(object):
    def __init__(self, lyrics):
        self.lyrics = lyrics
    def sing_me_song(self):
        for line in self.lyrics:
            print(line)

happy_bday = Song(["Happy birthday to you", "I don't want to get sued","So I'll stop right there"])
happy_bday.sing_me_song()