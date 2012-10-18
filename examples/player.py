"""OpenAL playback example."""
import os
import sys
import time
import wave
import openal

def run():
    if len (sys.argv) < 2:
        print ("Usage: %s wavefile" % os.path.basename(sys.argv[0]))
        print ("    Using an example wav file...")
        dirname = os.path.dirname(__file__)
        fname = os.path.join(dirname, "swoosh.wav")
    else:
        fname = sys.argv[1]

    wavefp = wave.open(fname)
    channels = wavefp.getnchannels()
    bitrate = wavefp.getsampwidth() * 8
    samplerate = wavefp.getframerate()
    wavbuf = wavefp.readframes(wavefp.getnframes())
    formatmap = {
        (1, 8) : openal.AL_FORMAT_MONO8,
        (2, 8) : openal.AL_FORMAT_STEREO8,
        (1, 16): openal.AL_FORMAT_MONO16,
        (2, 16) : openal.AL_FORMAT_STEREO16,
    }
    alformat = formatmap[(channels, bitrate)]

    device = openal.alcOpenDevice(None)
    context = openal.alcCreateContext(device, None)
    openal.alcMakeContextCurrent(context)

    source = openal.ALuint(0)
    openal.alGenSources(1, source)

    openal.alSourcef(source, openal.AL_PITCH, 1)
    openal.alSourcef(source, openal.AL_GAIN, 1)
    openal.alSource3f(source, openal.AL_POSITION, 10, 0, 0)
    openal.alSource3f(source, openal.AL_VELOCITY, 0, 0, 0)
    openal.alSourcei(source, openal.AL_LOOPING, 1)

    buf = openal.ALuint(0)
    openal.alGenBuffers(1, buf)

    openal.alBufferData(buf, alformat, wavbuf, len(wavbuf), samplerate)
    openal.alSourceQueueBuffers(source, 1, buf)
    openal.alSourcePlay(source)

    state = openal.ALint(0)
    openal.alGetSourcei(source, openal.AL_SOURCE_STATE, state)
    z = 10
    while z > -10:
        print("playing the file...")
        time.sleep(1)
        openal.alSource3f(source, openal.AL_POSITION, z, 0, 0)
        z -=1
    print("done")

    openal.alDeleteSources(1, source)
    openal.alDeleteBuffers(1, buf)
    openal.alcDestroyContext(context)
    openal.alcCloseDevice(device)

if __name__ == "__main__":
    sys.exit(run())
