
import os, hashlib, random

def fhash(fn):
	return hashlib.sha1(open(fn, "rb").read()).hexdigest()
def getid(o):
	return hashlib.sha1(o.encode('utf-8')).hexdigest()[:8]

class Song():
	def __init__(self, title, artist, album, tn, genre, ext, fmt, dur, rel, discn, bitr, fn):
		self._id = getid(title+"_"+album+"_"+artist)
		self._albumid = getid(album+"_"+artist)
		self._artistid = getid(artist)
		self._title = title
		self._artist = artist
		self._album = album
		self._tn = tn
		self._ext = ext
		self._fmt = fmt
		self._duration = dur
		self._genre = genre
		self._release = rel
		self._bitrate = bitr
		self._discn = discn
		self._file = os.path.realpath(fn)
	def __str__(self):
		return "%s: %s - %s (%s)" % (self._id, self._title, self._album, self._artist)

class Album():
	def __init__(self, artist, album):
		self._id = getid(album+"_"+artist)
		self._artistid = getid(artist)
		self._album = album
		self._artist = artist
		self._songs = []

	def addSong(self, s):
		for song in self._songs:
			if s._title == song._title:
				return

		self._songs.append(s)

	def getSongs(self):
		return { a._id:a for a in self._songs }

	def getAllSongs(self):
		r = {}
		for song in self._songs:
			r.update({ s._id:s for s in self._songs })
		return r

	def getRandom(self):
		s = random.choice(self._songs)
		return { s._id:s }

class Artist():
	def __init__(self, artist):
		self._id = getid(artist)
		self._artist = artist
		self._albums = []

	def addSong(self, s):
		al = None
		for album in self._albums:
			if s._album == album._album:
				al = album
				break
		if not al:
			al = Album(s._artist, s._album)
			self._albums.append(al)

		al.addSong(s)

	def getAlbums(self):
		return { a._id:a for a in self._albums }

	def getSongs(self, albid):
		for album in self._albums:
			if albid == album._id:
				return album.getSongs()
		return {}

	def getAllSongs(self):
		r = {}
		for album in self._albums:
			r.update( album.getAllSongs() )
		return r

	def getRandom(self):
		return random.choice(self._albums).getRandom()

class MusicDir():
	def __init__(self, modtime):
		self._artists = []
		self._modtime = modtime

	def addSong(self, s):
		ar = None
		for artist in self._artists:
			if s._artist == artist._artist:
				ar = artist
				break
		if not ar:
			ar = Artist(s._artist)
			self._artists.append(ar)

		ar.addSong(s)

	def getArtists(self):
		return { a._id:a._artist for a in self._artists }

	def getAllAlbums(self):
		r = {}
		for artist in self._artists:
			r.update( artist.getAlbums() )
		return r

	def getAllSongs(self):
		r = {}
		for artist in self._artists:
			r.update( artist.getAllSongs() )
		return r

	def getAlbums(self, art_id):
		for artist in self._artists:
			if art_id == artist._id:
				return artist.getAlbums()

	def getSongs(self, albid):
		r = {}
		for artist in self._artists:
			r.update(artist.getSongs(albid))
		return r

	def getRandom(self, n):
		r = {}
		for i in range(n):
			r.update(random.choice(self._artists).getRandom())
		return r


