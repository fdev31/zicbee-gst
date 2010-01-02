__all__ = ['Player']

import pygst
pygst.require('0.10')
import gst
import gobject, sys
from thread import start_new_thread
from time import time

class Player(object):
    _finished = True
    def __init__(self):
        self.p = None
        self.respawn()

        # FIXME: THIS IS A WORKAROUND SINCE on_message stuff is not working...
        self.last_position = 0
        self.last_position_ts = 0

    def set_cache(self, val):
        """ Sets the cache value in kilobytes """
        pass

    def volume(self, val):
        """ Sets volume [0-100] """
        self.p.props.volume = val/10.0

    def seek(self, val):
        """ Seeks specified number of seconds (positive or negative) """
        if self.p:
            pos = self._nano_pos + long(val)*1000000000

            self.p.seek(1.0, gst.FORMAT_TIME,
                 gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                 gst.SEEK_TYPE_SET, pos,
                 gst.SEEK_TYPE_NONE, 0)

    @property
    def paused(self):
        return gst.STATE_PAUSED in self.p.get_state()[1:]

    def pause(self):
        """ Toggles pause mode """
        if self.p:
            if self.paused:
                self.p.set_state(gst.STATE_PLAYING)
            else:
                self.p.set_state(gst.STATE_PAUSED)

    def respawn(self):
        """ Restarts the player """
        if self.p:
            self.p.set_state(gst.STATE_READY)
        self.p = gst.element_factory_make("playbin", "player")
        self.bus = self.p.get_bus()
        self.bus.connect('message', self.on_message)
        self.bus.add_signal_watch()

    def on_message(self, bus, message):
        t = message.type
        print repr(t)
        if t == gst.MESSAGE_ERROR:
            self._finished = True
        elif t == gst.MESSAGE_EOS:
            self._finished = True
#        elif t == gst.MESSAGE_STATE_CHANGED:
#            old, new, pending = message.parse_state_changed()
#            if old == gst.STATE_PLAYING:
#                self._finished = True
#            elif new == gst.STATE_PLAYING:
#                self._finished = False

    def load(self, uri):
        """ Loads the specified URI """
        if uri.startswith('/'):
            uri = 'file://%s'%uri

        self.p.set_state(gst.STATE_READY)
        self.p.set_property('uri', uri)
        self.p.set_state(gst.STATE_PLAYING)
        self._finished = False

    def quit(self):
        """ De-initialize player and wait for it to shut down """
        if self.p:
            try:
                self.p.set_state(gst.STATE_READY)
                self.p = None
            except Exception, e:
                print "E: %s"%e
            finally:
                gobject.MainLoop().quit()

    @property
    def position(self):
        """ returns the stream position, in seconds
        or None if not playing anymore
        """
        if self.p:
            if self._finished:
                return None
            try:
                p = int(self._nano_pos/1000000000.0 + 0.5)
                t = time()
                if p == self.last_position:
                    if self.last_position_ts + 2 < t:
                        if not self.paused:
                            return None
                else:
                    self.last_position = p
                    self.last_position_ts = t
                return p
            except:
                return None

    @property
    def _nano_pos(self):
        return self.p.query_position(gst.FORMAT_TIME)[0]


