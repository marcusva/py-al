"""Utility classes for OpenAL-based audio access."""
from collections import Iterable
from openal import *

__all__ = ["SoundListener", "SoundSource", "SoundData", "SoundSink",
           "OpenALError",
           ]


__version__ = "0.1.0"
version_info = (0, 1, 0, "")


# Helper functions
_to_ctypes = lambda seq, dtype: (len(seq) * dtype)(*seq)
_to_python = lambda seq: [x.value for x in seq]


# Error handling
_clear_error = lambda: alGetError()
_ERRMAP = {AL_NO_ERROR: "No Error",
           AL_INVALID_NAME: "Invalid name",
           AL_INVALID_ENUM: "Invalid enum",
           AL_INVALID_VALUE: "Invalid value",
           AL_INVALID_OPERATION: "Invalid operation",
           AL_OUT_OF_MEMORY: "Out of memory"
           }
_get_error_message = lambda x: _ERRMAP.get(x, "Error code [%d]" % x)


def _continue_or_raise():
    """Raises an OpenALError, if an error flag is set."""
    err = alGetError()
    if err != AL_NO_ERROR:
        raise OpenALError(get_error_message(err))


# Property update handling on SoundListener, SoundData and SoundSource
_SOURCEPROPMAP = {
    "pitch": AL_PITCH,
    "gain": AL_GAIN,
    "max_distance": AL_MAX_DISTANCE,
    "rolloff_factor": AL_ROLLOFF_FACTOR,
    "reference_distance": AL_REFERENCE_DISTANCE,
    "min_gain": AL_MIN_GAIN,
    "max_gain": AL_MAX_GAIN,
    "cone_outer_gain": AL_CONE_OUTER_GAIN,
    "cone_inner_angle": AL_CONE_INNER_ANGLE,
    "cone_outer_angle": AL_CONE_OUTER_ANGLE,
    "position": AL_POSITION,
    "velocity": AL_VELOCITY,
    "direction": AL_DIRECTION,
    "source_relative": AL_SOURCE_RELATIVE,
    "source_type": AL_SOURCE_TYPE,
    "looping": AL_LOOPING,
    "buffer": AL_BUFFER,
    "source_state": AL_SOURCE_STATE,
    "sec_offset": AL_SEC_OFFSET,
    "sample_offset": AL_SAMPLE_OFFSET,
    "byte_offset": AL_BYTE_OFFSET,
    "buffers_queued": AL_BUFFERS_QUEUED,
    "buffers_processed": AL_BUFFERS_PROCESSED,
    }

_LISTENERPROPMAP = {
    # Listener properties
    "orientation": AL_ORIENTATION,
    "position": AL_POSITION,
    "velocity": AL_VELOCITY,
    "gain": AL_GAIN,
    }

_BUFFERPROPMAP = {
    # Buffer properties
    "frequency": AL_FREQUENCY,
    "bits": AL_BITS,
    "channels": AL_CHANNELS,
    "size": AL_SIZE,
    }

_CTXPROPMAP = {
    # Context Manager properties
    "frequency": ALC_FREQUENCY,
    "mono_sources": ALC_MONO_SOURCES,
    "stereo_sources": ALC_STEREO_SOURCES,
    "refresh": ALC_REFRESH,
    "sync": ALC_SYNC,
    }

# The callbacks are
# ([elemcount, ]type setter, getter)
#
# For buffers in OpenAL 1.1 all props are specified as read-only, hence
# the SoundData structure ignores those information, but stores
# everything in properties, without interacting with OpenAL.
#
_BUFFERCALLBACKS = {
        AL_FREQUENCY: (ALint, alBufferi, alGetBufferi),
        AL_BITS: (ALint, alBufferi, alGetBufferi),
        AL_CHANNELS: (ALint, alBufferi, alGetBufferi),
        AL_SIZE: (ALint, alBufferi, alGetBufferi),
        }
def _get_buffer_value(bufid, prop):
    """Gets the requested OpenAL buffer property value."""
    _Type, setter, getter = _BUFFERCALLBACKS[prop]
    v = _Type()
    getter(bufid, prop, v)
    return v
def _set_buffer_value(bufid, prop, value):
    """Sets a OpenAL buffer property value."""
    _BUFFERCALLBACKS[prop][1](bufid, prop, value)


_LISTENERCALLBACKS = {
        AL_GAIN: (1, ALfloat, alListenerf, alListenerf, 1),
        AL_POSITION: (3, ALfloat, alListenerfv, alGetListenerfv),
        AL_VELOCITY: (3, ALfloat, alListenerfv, alGetListenerfv),
        AL_ORIENTATION: (6, ALfloat, alListenerfv, alGetListenerfv),
        }
def _get_listener_value(prop):
    """Gets the requested OpenAL listener property value."""
    size, _Type, setter, getter = _LISTENERCALLBACKS[prop]
    v = (_Type * size)()
    getter(prop, v)
    return v
def _set_listener_value(prop, value):
    """Sets a OpenAL listener property value."""
    size, _Type, setter, getter = _LISTENERCALLBACKS[prop]
    if size > 1:
        value = _to_ctypes(value, _Type)
    setter(prop, value)


_SOURCECALLBACKS = {
        AL_PITCH: (1, ALfloat, alSourcef, alGetSourcef),
        AL_GAIN: (1, ALfloat, alSourcef, alGetSourcef),
        AL_MAX_DISTANCE: (1, ALfloat, alSourcef, alGetSourcef),
        AL_ROLLOFF_FACTOR: (1, ALfloat, alSourcef, alGetSourcef),
        AL_REFERENCE_DISTANCE: (1, ALfloat, alSourcef, alGetSourcef),
        AL_MIN_GAIN: (1, ALfloat, alSourcef, alGetSourcef),
        AL_MAX_GAIN: (1, ALfloat, alSourcef, alGetSourcef),
        AL_CONE_OUTER_GAIN: (1, ALfloat, alSourcef, alGetSourcef),
        AL_CONE_INNER_ANGLE: (1, ALfloat, alSourcef, alGetSourcef),
        AL_CONE_OUTER_ANGLE: (1, ALfloat, alSourcef, alGetSourcef),
        AL_POSITION: (3, ALfloat, alSourcefv, alGetSourcefv),
        AL_VELOCITY: (3, ALfloat, alSourcefv, alGetSourcefv),
        AL_DIRECTION: (3, ALfloat, alSourcefv, alGetSourcefv),
        AL_SOURCE_RELATIVE: (1, ALint, alSourcei, alGetSourcei),
        AL_SOURCE_TYPE: (1, ALint, alSourcei, alGetSourcei),
        AL_LOOPING: (1, ALint, alSourcei, alGetSourcei),
        AL_SOURCE_STATE: (1, ALint, alSourcei, alGetSourcei),
        AL_BUFFERS_QUEUED: (1, ALint, None, alGetSourcei),
        AL_BUFFERS_PROCESSED: (1, ALint, None, alGetSourcei),
        AL_SEC_OFFSET: (1, ALfloat, alSourcef, alGetSourcef),
        AL_SAMPLE_OFFSET: (1, ALfloat, alSourcef, alGetSourcef),
        AL_BYTE_OFFSET: (1, ALfloat, alSourcef, alGetSourcef),
        }
def _get_source_value(sourceid, prop):
    """Gets the requested OpenAL source property value."""
    size, _Type, setter, getter = _SOURCECALLBACKS[prop]
    v = (_Type * size)()
    getter(sourceid, prop, v)
    return v
def _set_source_value(sourceid, prop, value):
    """Sets a OpenAL source property value."""
    size, _Type, setter, getter = _SOURCECALLBACKS[prop]
    if size > 1:
        value = _to_ctypes(value, _Type)
    setter(sourceid, prop, value)


class OpenALError(Exception):
    """A OpenAL specific exception class."""
    def __init__(self, msg=None):
        """Creates a new OpenALError instance with the specified message.

        If no msg is provided, the message will be set a mapped value of
        alGetError().
        """
        super(OpenALError, self).__init__()
        self.msg = msg
        self.errcode = -1
        if msg is None:
            self.errcode = alGetError()
            self.msg = _get_error_message(self.errcode)

    def __str__(self):
        return repr(self.msg)


class SoundData(object):
    """A buffered audio object.

    The SoundData consists of a PCM audio data buffer, the audio frequency
    and format information.
    """
    def __init__(self, data=None, channels=None, bitrate=None, size=None,
                 frequency=None):
        """Creates a new SoundData object."""
        self.channels = channels
        self.bitrate = bitrate
        self.size = size
        self.frequency = frequency
        self._data = data

    @property
    def data(self):
        """The PCM audio data."""
        return self._data

class StreamingSoundData(SoundData):
    """A streaming audio object.
    
    The StreamingSoundData consists of a PCM audio stream, the audio frequency
    and format information. It reads and fills a buffer automatically on
    underruns.
    """
    def __init__(self, stream=None, channels=None, bitrate=None, size=None,
                 frequency=None):
        """Creates a new StreamingSoundData object."""
        super(StreamingSoundData, self).__init__(None, channels, bitrate,
                                                 size, frequency)

    def read(self, size):
        pass
    
    def seek(self, position):
        pass

    def data(self):
        pass

class SoundListener(object):
    """A listener object within the 3D audio space."""
    def __init__(self, position=[0, 0, 0], velocity=[0, 0, 0],
                 orientation=[0, 0, -1, 0, 1, 0]):
        """Creates a new SoundListener with a specific position, movement
        velocity and hearing orientation."""
        self.dataproperties = {}
        self.dataproperties[AL_POSITION] = position
        self.dataproperties[AL_VELOCITY] = velocity
        self.dataproperties[AL_ORIENTATION] = orientation
        self.changedproperties = [AL_POSITION, AL_VELOCITY, AL_ORIENTATION]

    def __getattr__(self, name):
        if name in ("dataproperties", "changedproperties"):
            return super(SoundListener, self).__getattr__(name, value)
        dprop = _LISTENERPROPMAP.get(name, None)
        if dprop is None:
            raise AttributeError("object %r has no attribute %r" % \
                                     (self.__class__.__name__, name))
        # Either get the value or return None, if it has not been
        # fetched yet.
        return self.dataproperties.get(dprop, None)

    def __setattr__(self, name, value):
        if name in ("dataproperties", "changedproperties"):
            return super(SoundListener, self).__setattr__(name, value)
        dprop = _LISTENERPROPMAP.get(name, None)
        if dprop is None:
            raise AttributeError("object %r has no attribute %r" % \
                                     (self.__class__.__name__, name))
        self.dataproperties[dprop] = value
        if dprop not in self.changedproperties:
            self.changedproperties.append(dprop)

    def __delattr__(self, name):
        if name in ("dataproperties", "changedproperties"):
            return super(SoundListener, self).__delattr__(name, value)
        dprop = _LISTENERPROPMAP.get(name, None)
        if dprop is None:
            raise AttributeError("object %r has no attribute %r" % \
                                     (self.__class__.__name__, name))
        self.dataproperties.pop(dprop, None)

    @property
    def changed(self):
        """Indicates, if one or more properties changed since the last
        update."""
        return len(self.changedproperties) != 0


class SoundSource(object):
    """An object within the application world, which can emit sounds."""
    def __init__(self, gain=1.0, pitch=1.0, position=[0, 0, 0],
                 velocity=[0, 0, 0]):
        self.bufferqueue = []
        self.dataproperties = {}
        self.dataproperties[AL_GAIN] = gain
        self.dataproperties[AL_PITCH] = pitch
        self.dataproperties[AL_POSITION] = position
        self.dataproperties[AL_VELOCITY] = velocity
        self.changedproperties = [AL_GAIN, AL_PITCH, AL_POSITION, AL_VELOCITY]

    def __getattr__(self, name):
        if name in ("dataproperties", "changedproperties", "bufferqueue"):
            return super(SoundSource, self).__getattr__(name, value)
        dprop = _SOURCEPROPMAP.get(name, None)
        if dprop is None:
            raise AttributeError("object %r has no attribute %r" % \
                                     (self.__class__.__name__, name))
        # Either get the value or return None, if it has not been
        # fetched yet.
        return self.dataproperties.get(dprop, None)

    def __setattr__(self, name, value):
        if name in ("dataproperties", "changedproperties", "bufferqueue"):
            return super(SoundSource, self).__setattr__(name, value)
        dprop = _SOURCEPROPMAP.get(name, None)
        if dprop is None:
            raise AttributeError("object %r has no attribute %r" % \
                                     (self.__class__.__name__, name))
        self.dataproperties[dprop] = value
        if dprop not in self.changedproperties:
            self.changedproperties.append(dprop)

    def __delattr__(self, name):
        if name in ("dataproperties", "changedproperties", "bufferqueue"):
            return super(SoundSource, self).__delattr__(name, value)
        dprop = _SOURCEPROPMAP.get(name, None)
        if dprop is None:
            raise AttributeError("object %r has no attribute %r" % \
                                     (self.__class__.__name__, name))
        self.dataproperties.pop(dprop, None)

    @property
    def changed(self):
        """Indicates, that one or more properties changed since the last
        update."""
        return len(self.changedproperties) != 0

    def queue(self, sounddata):
        """Adds a SoundData object for playback to the SoundSource."""
        self.bufferqueue.append(sounddata)

    def play(self, sounddata):
        """Adds a SoundData object for playback to the SoundSource."""
        self.queue(sounddata)


class SoundSink(object):
    """Audio playback system.

    The SoundSink handles audio output for sound sources. It connects to an
    audio output device and manages the source settings, buffer queues and
    the playback of them.
    """
    def __init__(self, device=None, attributes=None):
        """Creates a new SoundSink for a specific audio output device."""
        if isinstance(device, ALCdevice):
            self.device = device
            self._deviceopened = False
        else:
            self._deviceopened = True
            device = alcOpenDevice(device)
            if device is None:
                raise OpenALError()
            self.device = device.contents
        if attributes:
            attributes = _to_ctypes(attributes, ALCint)
        context = alcCreateContext(device, attributes)
        if not context:
            raise OpenALError()
        self.context = context.contents
        
        self._sources = {}
        self._sids = {}
        self._listener = None

    def __del__(self):
        context = getattr(self, "context", None)
        if context:
            alcDestroyContext(context)
        self.context = None
        if self._deviceopened:
            alcCloseDevice(self.device)
        self.device = None

    def activate(self):
        """Marks the SoundSink as being the current one for operating on
        the OpenAL states."""
        alcMakeContextCurrent(self.context)

    @property
    def listener(self):
        """Gets or sets the SoundListener of the SoundSink."""
        if self._listener is None:
            self._listener = SoundListener()
        return self._listener

    @listener.setter
    def listener(self, value):
        """Gets or sets the SoundListener of the SoundSink."""
        self._listener = value

    @property
    def opened_device(self):
        """Gets, whether the SoundSink initially opened the device."""
        return self._deviceopened

    def refresh(self, source):
        """Refreshes the passed SoundSource's internal state."""
        sid = self._sources.get(source, None)
        if sid is None:
            raise ValueError("source not associated with the SoundSink")
        for key in _SOURCECALLBACKS:
            source.dataproperties[key] = _to_python(_get_source_value(sid, key))

    def _create_source_id(self, source):
        """Creates a OpenAL source id for the passed SoundSource."""
        if source in self._sources:
            # We should have a OpenAL source id already
            return self._sources[source]
        # None yet, create a new one or bind it to an existing id
        sid = None
        for p, v in self._sids.items():
            if v is None:
                # Unused sid, use that one
                sid = p
        if not sid:
            sid = ALuint()
            alGenSources(1, sid)
            _continue_or_raise()
        self._sources[source] = sid.value
        print 
        self._sids[sid.value] = source
        return sid.value

    def play(self, sources):
        """Starts playing the buffered sounds of the source or sources."""
        if isinstance(sources, Iterable):
            sids = []
            for source in sources:
                sids.append(self._create_source_id(source))
            alSourcePlayv(_to_ctypes(sids, ALuint), len(sids))
        else:
            sid = self._create_source_id(sources)
            alSourcePlay(sid)

    def stop(self, sources):
        """Stops playing the buffered sounds of the source or sources."""
        if isinstance(sources, Iterable):
            sids = [self._sources[source] for source in sources
                    if source in self._sources]
            alSourceStopv(_to_ctypes(sids, ALuint), len(sids))
        elif sources in self._sources:
            alSourceStop(self._sources[source])

    def pause(self, sources):
        """Pauses the playback of the buffered sounds of the source or
        sources."""
        if isinstance(sources, Iterable):
            sids = [self._sources[source] for source in sources
                    if source in self._sources]
            alSourcePausev(_to_ctypes(sids, ALuint), len(sids))
        elif sources in self._sources:
            alSourcePause(self._sources[source])

    def rewind(self, sources):
        """Rewinds the buffers of the source or sources."""
        if isinstance(sources, Iterable):
            sids = [self._sources[source] for source in sources
                    if source in self._sources]
            alSourceRewindv(_to_ctypes(sids, ALuint), len(sids))
        elif sources in self._sources:
            alSourceRewind(self._sources[source])

    def process_source(self, source):
        """Processes the passed SoundSource."""
        sid = self._create_source_id(source)
        # Apply the changed information of the source, if any
        props = getattr(source, "changedproperties", [])
        for prop in props:
            _set_source_value(sid, prop, source.dataproperties[prop])
        source.changedproperties = []

    def process_listener(self):
        """Processes the SoundListener attached to the SoundSink."""
        props = getattr(self.listener, "changedproperties", [])
        for prop in props:
            _set_listener_value(prop, self.listener.dataproperties[prop])
        self.listener.changedproperties = []
        
    def update(self):
        """Processes all currently attached sound sources."""
        self.process_listener()
        process_source = self.process_source
        for source in self._sources:
            process_source(source)
