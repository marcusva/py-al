"""OpenAL AL and ALC wrapper"""
import os
import sys
import ctypes
import warnings
from ctypes.util import find_library

__all__ = ["get_dll_file",

           "AL_INVALID", "AL_NONE", "AL_TRUE", "AL_FALSE",
           "AL_SOURCE_RELATIVE", "AL_CONE_INNER_ANGLE", "AL_CONE_OUTER_ANGLE",
           "AL_PITCH", "AL_POSITION", "AL_DIRECTION", "AL_VELOCITY",
           "AL_LOOPING", "AL_BUFFER", "AL_GAIN", "AL_MIN_GAIN", "AL_MAX_GAIN",
           "AL_ORIENTATION", "AL_CHANNEL_MASK", "AL_SOURCE_STATE",
           "AL_INITIAL", "AL_PLAYING", "AL_PAUSED", "AL_STOPPED",
           "AL_BUFFERS_QUEUED", "AL_BUFFERS_PROCESSED", "AL_SEC_OFFSET",
           "AL_SAMPLE_OFFSET", "AL_BYTE_OFFSET", "AL_SOURCE_TYPE",
           "AL_STATIC", "AL_STREAMING", "AL_UNDETERMINED", "AL_FORMAT_MONO8",
           "AL_FORMAT_MONO16", "AL_FORMAT_STEREO8", "AL_FORMAT_STEREO16",
           "AL_REFERENCE_DISTANCE", "AL_ROLLOFF_FACTOR", "AL_CONE_OUTER_GAIN",
           "AL_MAX_DISTANCE", "AL_FREQUENCY", "AL_BITS", "AL_CHANNELS",
           "AL_SIZE", "AL_UNUSED", "AL_PENDING", "AL_PROCESSED", "AL_NO_ERROR",
           "AL_INVALID_NAME", "AL_ILLEGAL_ENUM", "AL_INVALID_ENUM",
           "AL_INVALID_VALUE", "AL_ILLEGAL_COMMAND", "AL_INVALID_OPERATION",
           "AL_OUT_OF_MEMORY", "AL_VENDOR", "AL_VERSION", "AL_RENDERER",
           "AL_EXTENSIONS", "AL_DOPPLER_FACTOR", "AL_DOPPLER_VELOCITY",
           "AL_SPEED_OF_SOUND", "AL_DISTANCE_MODEL", "AL_INVERSE_DISTANCE",
           "AL_INVERSE_DISTANCE_CLAMPED", "AL_LINEAR_DISTANCE",
           "AL_LINEAR_DISTANCE_CLAMPED", "AL_EXPONENT_DISTANCE",
           "AL_EXPONENT_DISTANCE_CLAMPED", "ALboolean", "ALchar", "ALbyte",
           "ALubyte", "ALshort", "ALushort", "ALint", "ALuint", "ALsizei",
           "ALenum", "ALfloat", "ALdouble",  "ALvoid",
           "alEnable", "alDisable", "alIsEnabled", "alGetString",
           "alGetBooleanv", "alGetIntegerv", "alGetFloatv", "alGetDoublev",
           "alGetBoolean", "alGetInteger", "alGetFloat", "alGetDouble",
           "alGetError", "alIsExtensionPresent", "alGetProcAddress",
           "alGetEnumValue", "alListenerf", "alListener3f", "alListenerfv",
           "alListeneri", "alListener3i", "alListeneriv", "alGetListenerf",
           "alGetListener3f", "alGetListenerfv", "alGetListeneri",
           "alGetListener3i", "alGetListeneriv", "alGenSources",
           "alDeleteSources", "alIsSource", "alSourcef", "alSource3f",
           "alSourcefv", "alSourcei", "alSource3i", "alSourceiv",
           "alGetSourcef", "alGetSource3f", "alGetSourcefv", "alGetSourcei",
           "alGetSource3i", "alGetSourceiv", "alSourcePlayv", "alSourcePlay",
           "alSourceStopv", "alSourceStop", "alSourceRewindv",
           "alSourceRewind", "alSourcePausev", "alSourcePause",
           "alSourceQueueBuffers", "alSourceUnqueueBuffers", "alGenBuffers",
           "alIsBuffer", "alBufferData", "alBufferf", "alBuffer3f",
           "alBufferfv", "alBufferi", "alBuffer3i", "alBufferiv",
           "alGetBufferf", "alGetBuffer3f", "alGetBufferfv", "alGetBufferi",
           "alGetBuffer3i", "alGetBufferiv", "alDopplerFactor",
           "alDopplerVelocity", "alSpeedOfSound", "alDistanceModel",

           "ALC_FALSE", "ALC_TRUE", "ALC_INVALID", "ALC_FREQUENCY",
           "ALC_REFRESH", "ALC_SYNC", "ALC_MONO_SOURCES", "ALC_STEREO_SOURCES",
           "ALC_NO_ERROR", "ALC_INVALID_DEVICE", "ALC_INVALID_CONTEXT",
           "ALC_INVALID_ENUM", "ALC_INVALID_VALUE", "ALC_OUT_OF_MEMORY",
           "ALC_DEFAULT_DEVICE_SPECIFIER", "ALC_DEVICE_SPECIFIER",
           "ALC_EXTENSIONS", "ALC_MAJOR_VERSION", "ALC_MINOR_VERSION",
           "ALC_ATTRIBUTES_SIZE", "ALC_ALL_ATTRIBUTES",
           "ALC_DEFAULT_ALL_DEVICES_SPECIFIER", "ALC_ALL_DEVICES_SPECIFIER",
           "ALC_CAPTURE_DEVICE_SPECIFIER",
           "ALC_CAPTURE_DEFAULT_DEVICE_SPECIFIER", "ALC_CAPTURE_SAMPLES",
           "ALCboolean", "ALCchar", "ALCbyte", "ALCubyte", "ALCshort",
           "ALCushort", "ALCint", "ALCuint", "ALCsizei", "ALCenum", "ALCfloat",
           "ALCdouble", "ALCvoid", "ALCdevice", "ALCcontext",
           "alcCreateContext", "alcMakeContextCurrent", "alcProcessContext",
           "alcSuspendContext", "alcDestroyContext", "alcGetCurrentContext",
           "alcGetContextsDevice", "alcOpenDevice", "alcCloseDevice",
           "alcGetError", "alcIsExtensionPresent", "alcGetProcAddress",
           "alcGetEnumValue", "alcGetString", "alcGetIntegerv",
           "alcCaptureOpenDevice", "alcCaptureCloseDevice", "alcCaptureStart",
           "alcCaptureStop", "alcCaptureSamples"
           ]


__version__ = "0.1.0"
version_info = (0, 1, 0, "")


def _findlib(libnames, path=None):
    """."""
    platform = sys.platform
    if platform in ("win32", "cli"):
        suffix = ".dll"
    elif platform == "darwin":
        suffix = ".dylib"
    else:
        suffix = ".so"

    searchfor = libnames
    if type(libnames) is dict:
        # different library names for the platforms
        if platform == "cli" and platform not in libnames:
            # if not explicitly specified, use the Win32 libs for IronPython
            platform = "win32"
        if platform not in libnames:
            platform = "DEFAULT"
        searchfor = libnames[platform]
    results = []
    if path:
        for libname in searchfor:
            dllfile = os.path.join(path, "%s%s" % (libname, suffix))
            if os.path.exists(dllfile):
                results.append(dllfile)
    for libname in searchfor:
        dllfile = find_library(libname)
        if dllfile:
            results.append(dllfile)
    return results


class _DLL(object):
    """Function wrapper around the different DLL functions. Do not use or
    instantiate this one directly from your user code.
    """
    def __init__(self, libinfo, libnames, path=None):
        self._dll = None
        foundlibs = _findlib(libnames, path)
        if len(foundlibs) == 0:
            raise RuntimeError("could not find any library for %s" % libinfo)
        for libfile in foundlibs:
            try:
                self._dll = ctypes.CDLL(libfile)
                self._libfile = libfile
                break
            except Exception as exc:
                # Could not load it, silently ignore that issue and move
                # to the next one.
                warnings.warn(exc, ImportWarning)
        if self._dll is None:
            raise RuntimeError("could not load any library for %s" % libinfo)

    def bind_function(self, funcname, args=None, returns=None):
        """Binds the passed argument and return value types to the specified
        function."""
        func = getattr(self._dll, funcname)
        func.argtypes = args
        func.restype = returns
        return func

    @property
    def libfile(self):
        """Gets the filename of the loaded library."""
        return self._libfile


dll = _DLL("OpenAL", {"win32": ["OpenAL", "OpenAL32"],
                      "darwin": ["OpenAL"],
                      "DEFAULT": ["openal", "OpenAL"]},
           os.getenv("PYAL_DLL_PATH"))


def get_dll_file():
    """Gets the file name of the loaded OpenAL library."""
    return dll.libfile


AL_INVALID = -1
AL_NONE = 0

AL_FALSE = 0
AL_TRUE =  1

AL_SOURCE_RELATIVE = 0x202

AL_CONE_INNER_ANGLE = 0x1001
AL_CONE_OUTER_ANGLE = 0x1002
AL_PITCH =            0x1003
AL_POSITION =         0x1004
AL_DIRECTION =        0x1005
AL_VELOCITY =         0x1006
AL_LOOPING =          0x1007
AL_BUFFER =           0x1009
AL_GAIN =             0x100A
AL_MIN_GAIN =         0x100D
AL_MAX_GAIN =         0x100E
AL_ORIENTATION =      0x100F

AL_CHANNEL_MASK = 0x3000

AL_SOURCE_STATE =      0x1010
AL_INITIAL =           0x1011
AL_PLAYING =           0x1012
AL_PAUSED =            0x1013
AL_STOPPED =           0x1014
AL_BUFFERS_QUEUED =    0x1015
AL_BUFFERS_PROCESSED = 0x1016

AL_SEC_OFFSET =    0x1024
AL_SAMPLE_OFFSET = 0x1025
AL_BYTE_OFFSET =   0x1026
AL_SOURCE_TYPE =   0x1027
AL_STATIC =        0x1028
AL_STREAMING =     0x1029
AL_UNDETERMINED =  0x1030

AL_FORMAT_MONO8 =    0x1100
AL_FORMAT_MONO16 =   0x1101
AL_FORMAT_STEREO8 =  0x1102
AL_FORMAT_STEREO16 = 0x1103

AL_REFERENCE_DISTANCE = 0x1020
AL_ROLLOFF_FACTOR =     0x1021
AL_CONE_OUTER_GAIN =    0x1022
AL_MAX_DISTANCE =       0x1023

AL_FREQUENCY = 0x2001
AL_BITS =      0x2002
AL_CHANNELS =  0x2003
AL_SIZE =      0x2004

AL_UNUSED =    0x2010
AL_PENDING =   0x2011
AL_PROCESSED = 0x2012

AL_NO_ERROR =          AL_FALSE
AL_INVALID_NAME =      0xA001
AL_ILLEGAL_ENUM =      0xA002
AL_INVALID_ENUM =      0xA002
AL_INVALID_VALUE =     0xA003
AL_ILLEGAL_COMMAND =   0xA004
AL_INVALID_OPERATION = 0xA004
AL_OUT_OF_MEMORY =     0xA005

AL_VENDOR =     0xB001
AL_VERSION =    0xB002
AL_RENDERER =   0xB003
AL_EXTENSIONS = 0xB004

AL_DOPPLER_FACTOR =   0xC000
AL_DOPPLER_VELOCITY = 0xC001
AL_SPEED_OF_SOUND =   0xC003

AL_DISTANCE_MODEL =            0xD000
AL_INVERSE_DISTANCE =          0xD001
AL_INVERSE_DISTANCE_CLAMPED =  0xD002
AL_LINEAR_DISTANCE =           0xD003
AL_LINEAR_DISTANCE_CLAMPED =   0xD004
AL_EXPONENT_DISTANCE =         0xD005
AL_EXPONENT_DISTANCE_CLAMPED = 0xD006

ALboolean = ctypes.c_char
ALchar = ctypes.c_char
ALbyte = ctypes.c_char
ALubyte = ctypes.c_ubyte
ALshort = ctypes.c_short
ALushort = ctypes.c_ushort
ALint = ctypes.c_int
ALuint = ctypes.c_uint
ALsizei = ctypes.c_int
ALenum = ctypes.c_int
ALfloat = ctypes.c_float
ALdouble = ctypes.c_double
ALvoid = None

_bind = dll.bind_function

alEnable = _bind("alEnable", [ALenum])
alDisable = _bind("alDisable", [ALenum])
alIsEnabled = _bind("alIsEnabled", [ALenum], ALboolean)
alGetString = _bind("alGetString", [ALenum], ctypes.POINTER(ALchar))
alGetBooleanv = _bind("alGetBooleanv", [ALenum, ctypes.POINTER(ALboolean)])
alGetIntegerv = _bind("alGetIntegerv", [ALenum, ctypes.POINTER(ALint)])
alGetFloatv = _bind("alGetFloatv", [ALenum, ctypes.POINTER(ALfloat)])
alGetDoublev = _bind("alGetDoublev", [ALenum, ctypes.POINTER(ALdouble)])
alGetBoolean = _bind("alGetBoolean", [ALenum], ALboolean)
alGetInteger = _bind("alGetInteger", [ALenum], ALint)
alGetFloat = _bind("alGetFloat", [ALenum], ALfloat)
alGetDouble = _bind("alGetDouble", [ALenum], ALdouble)
alGetError = _bind("alGetError", None, ALenum)
alIsExtensionPresent = _bind("alIsExtensionPresent",
                             [ctypes.POINTER(ALchar)], ALboolean)
alGetProcAddress = _bind("alGetProcAddress",
                         [ctypes.POINTER(ALchar)], ctypes.c_void_p)
alGetEnumValue = _bind("alGetEnumValue", [ctypes.POINTER(ALchar)], ALenum)
alListenerf = _bind("alListenerf", [ALenum, ALfloat])
alListener3f = _bind("alListener3f", [ALenum, ALfloat, ALfloat, ALfloat])
alListenerfv = _bind("alListenerfv", [ALenum, ctypes.POINTER(ALfloat)])
alListeneri = _bind("alListeneri", [ALenum, ALint])
alListener3i = _bind("alListener3i", [ALenum, ALint, ALint, ALint])
alListeneriv = _bind("alListeneriv", [ALenum, ctypes.POINTER(ALint)])
alGetListenerf = _bind("alGetListenerf", [ALenum, ctypes.POINTER(ALfloat)])
alGetListener3f = _bind("alGetListener3f", [ALenum, ctypes.POINTER(ALfloat),
                                            ctypes.POINTER(ALfloat),
                                            ctypes.POINTER(ALfloat)])
alGetListenerfv = _bind("alGetListenerfv", [ALenum, ctypes.POINTER(ALfloat)])
alGetListeneri = _bind("alGetListeneri", [ALenum, ctypes.POINTER(ALint)])
alGetListener3i = _bind("alGetListener3i", [ALenum, ctypes.POINTER(ALint),
                                            ctypes.POINTER(ALint),
                                            ctypes.POINTER(ALint)])
alGetListeneriv = _bind("alGetListeneriv", [ALenum, ctypes.POINTER(ALint)])
alGenSources = _bind("alGenSources", [ALsizei, ctypes.POINTER(ALuint)])
alDeleteSources = _bind("alDeleteSources", [ALsizei, ctypes.POINTER(ALuint)])
alIsSource = _bind("alIsSource", [ALuint], ALboolean)
alSourcef = _bind("alSourcef", [ALuint, ALenum, ALfloat])
alSource3f = _bind("alSource3f", [ALuint, ALenum, ALfloat, ALfloat, ALfloat])
alSourcefv = _bind("alSourcefv", [ALuint, ALenum, ctypes.POINTER(ALfloat)])
alSourcei = _bind("alSourcei", [ALuint, ALenum, ALint])
alSource3i = _bind("alSource3i", [ALuint, ALenum, ALint, ALint, ALint])
alSourceiv = _bind("alSourceiv", [ALuint, ALenum, ctypes.POINTER(ALint)])
alGetSourcef = _bind("alGetSourcef", [ALuint, ALenum, ctypes.POINTER(ALfloat)])
alGetSource3f = _bind("alGetSource3f", [ALuint, ALenum, ctypes.POINTER(ALfloat),
                                        ctypes.POINTER(ALfloat),
                                        ctypes.POINTER(ALfloat)])
alGetSourcefv = _bind("alGetSourcefv", [ALuint, ALenum,
                                        ctypes.POINTER(ALfloat)])
alGetSourcei = _bind("alGetSourcei", [ALuint, ALenum, ctypes.POINTER(ALint)])
alGetSource3i = _bind("alGetSource3i", [ALuint, ALenum, ctypes.POINTER(ALint),
                                        ctypes.POINTER(ALint),
                                        ctypes.POINTER(ALint)])
alGetSourceiv = _bind("alGetSourceiv", [ALuint, ALenum, ctypes.POINTER(ALint)])
alSourcePlayv = _bind("alSourcePlayv", [ALsizei, ctypes.POINTER(ALuint)])
alSourceStopv = _bind("alSourceStopv", [ALsizei, ctypes.POINTER(ALuint)])
alSourceRewindv = _bind("alSourceRewindv", [ALsizei, ctypes.POINTER(ALuint)])
alSourcePausev = _bind("alSourcePausev", [ALsizei, ctypes.POINTER(ALuint)])
alSourcePlay = _bind("alSourcePlay", [ALuint])
alSourceStop = _bind("alSourceStop", [ALuint])
alSourceRewind = _bind("alSourceRewind", [ALuint])
alSourcePause = _bind("alSourcePause", [ALuint])
alSourceQueueBuffers = _bind("alSourceQueueBuffers",
                             [ALuint, ALsizei, ctypes.POINTER(ALuint)])
alSourceUnqueueBuffers = _bind("alSourceUnqueueBuffers",
                               [ALuint, ALsizei, ctypes.POINTER(ALuint)])
alGenBuffers = _bind("alGenBuffers", [ALsizei, ctypes.POINTER(ALuint)])
alDeleteBuffers = _bind("alDeleteBuffers", [ALsizei, ctypes.POINTER(ALuint)])
alIsBuffer = _bind("alIsBuffer", [ALuint], ALboolean)
alBufferData = _bind("alBufferData", [ALuint, ALenum, ctypes.POINTER(ALvoid),
                                      ALsizei, ALsizei])
alBufferf = _bind("alBufferf", [ALuint, ALenum, ALfloat])
alBuffer3f = _bind("alBuffer3f", [ALuint, ALenum, ALfloat, ALfloat, ALfloat])
alBufferfv = _bind("alBufferfv", [ALuint, ALenum, ctypes.POINTER(ALfloat)])
alBufferi = _bind("alBufferi", [ALuint, ALenum, ALint])
alBuffer3i = _bind("alBuffer3i", [ALuint, ALenum, ALint, ALint, ALint])
alBufferiv = _bind("alBufferiv", [ALuint, ALenum, ctypes.POINTER(ALint)])
alGetBufferf = _bind("alGetBufferf", [ALuint, ALenum, ctypes.POINTER(ALfloat)])
alGetBuffer3f = _bind("alGetBuffer3f", [ALuint, ALenum,
                                        ctypes.POINTER(ALfloat),
                                        ctypes.POINTER(ALfloat),
                                        ctypes.POINTER(ALfloat)])
alGetBufferfv = _bind("alGetBufferfv", [ALuint, ALenum,
                                        ctypes.POINTER(ALfloat)])
alGetBufferi = _bind("alGetBufferi", [ALuint, ALenum, ctypes.POINTER(ALint)])
alGetBuffer3i = _bind("alGetBuffer3i", [ALuint, ALenum,
                                        ctypes.POINTER(ALint),
                                        ctypes.POINTER(ALint),
                                        ctypes.POINTER(ALint)])
alGetBufferiv = _bind("alGetBufferiv", [ALuint, ALenum, ctypes.POINTER(ALint)])
alDopplerFactor = _bind("alDopplerFactor", [ALfloat])
alDopplerVelocity = _bind("alDopplerVelocity", [ALfloat])
alSpeedOfSound = _bind("alSpeedOfSound", [ALfloat])
alDistanceModel = _bind("alDistanceModel", [ALenum])


ALC_INVALID = 0
ALC_FALSE = 0
ALC_TRUE =  1

ALC_FREQUENCY = 0x1007
ALC_REFRESH   = 0x1008
ALC_SYNC      = 0x1009

ALC_MONO_SOURCES =   0x1010
ALC_STEREO_SOURCES = 0x1011

ALC_NO_ERROR =        ALC_FALSE
ALC_INVALID_DEVICE  = 0xA001
ALC_INVALID_CONTEXT = 0xA002
ALC_INVALID_ENUM    = 0xA003
ALC_INVALID_VALUE   = 0xA004
ALC_OUT_OF_MEMORY   = 0xA005

ALC_DEFAULT_DEVICE_SPECIFIER = 0x1004
ALC_DEVICE_SPECIFIER =         0x1005
ALC_EXTENSIONS =               0x1006

ALC_MAJOR_VERSION = 0x1000
ALC_MINOR_VERSION = 0x1001

ALC_ATTRIBUTES_SIZE = 0x1002
ALC_ALL_ATTRIBUTES =  0x1003

ALC_DEFAULT_ALL_DEVICES_SPECIFIER = 0x1012
ALC_ALL_DEVICES_SPECIFIER =         0x1013

ALC_CAPTURE_DEVICE_SPECIFIER =         0x310
ALC_CAPTURE_DEFAULT_DEVICE_SPECIFIER = 0x311
ALC_CAPTURE_SAMPLES =                  0x312

ALCboolean = ctypes.c_char
ALCchar = ctypes.c_char
ALCbyte = ctypes.c_char
ALCubyte = ctypes.c_ubyte
ALCshort = ctypes.c_short
ALCushort = ctypes.c_ushort
ALCint = ctypes.c_int
ALCuint = ctypes.c_uint
ALCsizei = ctypes.c_int
ALCenum = ctypes.c_int
ALCfloat = ctypes.c_float
ALCdouble = ctypes.c_double
ALCvoid = None


class ALCdevice(ctypes.Structure):
    """An OpenAL device used for audio operations."""
    pass


class ALCcontext(ctypes.Structure):
    """An execution context on a OpenAL device."""
    pass

alcCreateContext = _bind("alcCreateContext", [ctypes.POINTER(ALCdevice),
                                              ctypes.POINTER(ALCint)],
                         ctypes.POINTER(ALCcontext))
alcMakeContextCurrent = _bind("alcMakeContextCurrent",
                              [ctypes.POINTER(ALCcontext)], ALCboolean)
alcProcessContext = _bind("alcProcessContext", [ctypes.POINTER(ALCcontext)])
alcSuspendContext = _bind("alcSuspendContext", [ctypes.POINTER(ALCcontext)])
alcDestroyContext = _bind("alcDestroyContext", [ctypes.POINTER(ALCcontext)])
alcGetCurrentContext = _bind("alcGetCurrentContext", None,
                             ctypes.POINTER(ALCcontext))
alcGetContextsDevice = _bind("alcGetContextsDevice",
                             [ctypes.POINTER(ALCcontext)],
                             ctypes.POINTER(ALCdevice))
alcOpenDevice = _bind("alcOpenDevice", [ctypes.POINTER(ALCchar)],
                      ctypes.POINTER(ALCdevice))
alcCloseDevice = _bind("alcCloseDevice", [ctypes.POINTER(ALCdevice)],
                       ALCboolean)
alcGetError = _bind("alcGetError", [ctypes.POINTER(ALCdevice)], ALCenum)
alcIsExtensionPresent = _bind("alcIsExtensionPresent",
                              [ctypes.POINTER(ALCdevice),
                               ctypes.POINTER(ALCchar)])
alcGetProcAddress = _bind("alcGetProcAddress", [ctypes.POINTER(ALCdevice),
                                                ctypes.POINTER(ALCchar)],
                          ctypes.c_void_p)
alcGetEnumValue = _bind("alcGetEnumValue", [ctypes.POINTER(ALCdevice),
                                            ctypes.POINTER(ALCchar)], ALCenum)
alcGetString = _bind("alcGetString", [ctypes.POINTER(ALCdevice), ALCenum],
                     ctypes.POINTER(ALCchar))
alcGetIntegerv = _bind("alcGetIntegerv", [ctypes.POINTER(ALCdevice),
                                          ALCenum, ALCsizei,
                                          ctypes.POINTER(ALCint)])
alcCaptureOpenDevice = _bind("alcCaptureOpenDevice",
                             [ctypes.POINTER(ALCchar), ALCuint, ALCenum,
                              ALCsizei], ctypes.POINTER(ALCdevice))
alcCaptureCloseDevice = _bind("alcCaptureCloseDevice",
                              [ctypes.POINTER(ALCdevice)])
alcCaptureStart = _bind("alcCaptureStart", [ctypes.POINTER(ALCdevice)])
alcCaptureStop = _bind("alcCaptureStop", [ctypes.POINTER(ALCdevice)])
alcCaptureSamples = _bind("alcCaptureSamples", [ctypes.POINTER(ALCdevice),
                                                ctypes.POINTER(ALCvoid),
                                                ALCsizei])
