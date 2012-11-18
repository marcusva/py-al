import sys
import unittest
from openal import *
from openalaudio import *


class OpenALAudioTest(unittest.TestCase):
    def setUp(self):
        if sys.version.startswith("3.1"):
            self.assertIsInstance = \
                lambda x, t: self.assertTrue(isinstance(x, t))

    def tearDown(self):
        pass

    def test_OpenALError(self):
        err = OpenALError()
        self.assertIsInstance(err, Exception)
        self.assertNotEqual(err.errcode, -1)
        self.assertIsNotNone(err.msg)

        err = OpenALError("test")
        self.assertIsInstance(err, Exception)
        self.assertEqual(err.errcode, -1)
        self.assertEqual(err.msg, "test")

    def test_SoundData(self):
        data = SoundData()
        self.assertIsInstance(data, SoundData)
        self.assertIsNone(data.frequency)
        self.assertIsNone(data.size)
        self.assertIsNone(data.channels)
        self.assertIsNone(data.data)
        self.assertIsNone(data.bitrate)
        # TODO: initializers

    def test_SoundData_frequency(self):
        data = SoundData()
        vals = ("test", 1, -1, None, self)
        for v in vals:
            data.frequency = v
            self.assertEqual(data.frequency, v)

    def test_SoundData_size(self):
        data = SoundData()
        vals = ("test", 1, -1, None, self)
        for v in vals:
            data.size = v
            self.assertEqual(data.size, v)

    def test_SoundData_channels(self):
        data = SoundData()
        vals = ("test", 1, -1, None, self)
        for v in vals:
            data.channels = v
            self.assertEqual(data.channels, v)

    def test_SoundData_data(self):
        data = SoundData()
        vals = ("test", 1, -1, None, self)
        for v in vals:
            data.data = v
            self.assertEqual(data.data, v)

    def test_SoundData_bitrate(self):
        data = SoundData()
        vals = ("test", 1, -1, None, self)
        for v in vals:
            data.bitrate = v
            self.assertEqual(data.bitrate, v)

    def test_SoundListener(self):
        listener = SoundListener()
        self.assertIsInstance(listener, SoundListener)
        self.assertEqual(listener.position, (0, 0, 0))
        self.assertEqual(listener.velocity, (0, 0, 0))
        self.assertEqual(listener.orientation, (0, 0, -1, 0, 1, 0))
        self.assertEqual(listener.position,
                         listener.dataproperties[AL_POSITION])
        self.assertEqual(listener.velocity,
                         listener.dataproperties[AL_VELOCITY])
        self.assertEqual(listener.orientation,
                         listener.dataproperties[AL_ORIENTATION])
        self.assertTrue(listener.changed)

    def test_SoundListener_props(self):
        vals = ("test", 1, -1, None, self)
        props = [("position", AL_POSITION),
                 ("velocity", AL_VELOCITY),
                 ("orientation", AL_ORIENTATION),
                 ]

        listener = SoundListener()
        for v in vals:
            for name, dprop in props:
                listener.changedproperties = []
                self.assertFalse(listener.changed)
                setattr(listener, name, v)
                self.assertEqual(getattr(listener, name), v)
                self.assertEqual(listener.dataproperties[dprop], v)
                self.assertTrue(listener.changed)
                self.assertTrue(dprop in listener.changedproperties)

    def test_SoundSource(self):
        source = SoundSource()
        self.assertIsInstance(source, SoundSource)
        self.assertEqual(source.pitch, 1.0)
        self.assertEqual(source.gain, 1.0)
        self.assertEqual(source.position, (0, 0, 0))
        self.assertEqual(source.velocity, (0, 0 ,0))
        self.assertEqual(source.pitch, source.dataproperties[AL_PITCH])
        self.assertEqual(source.gain, source.dataproperties[AL_GAIN])
        self.assertEqual(source.position, source.dataproperties[AL_POSITION])
        self.assertEqual(source.velocity, source.dataproperties[AL_VELOCITY])
        self.assertTrue(source.changed)

    def test_SoundSource_props(self):
        vals = ("test", 1, -1, None, self)
        props = [("pitch", AL_PITCH),
                 ("gain", AL_GAIN),
                 ("max_distance", AL_MAX_DISTANCE),
                 ("rolloff_factor", AL_ROLLOFF_FACTOR),
                 ("reference_distance", AL_REFERENCE_DISTANCE),
                 ("min_gain", AL_MIN_GAIN),
                 ("max_gain", AL_MAX_GAIN),
                 ("cone_outer_gain", AL_CONE_OUTER_GAIN),
                 ("cone_outer_angle", AL_CONE_OUTER_ANGLE),
                 ("cone_inner_angle", AL_CONE_INNER_ANGLE),
                 ("position", AL_POSITION),
                 ("velocity", AL_VELOCITY),
                 ("direction", AL_DIRECTION),
                 ("source_relative", AL_SOURCE_RELATIVE),
                 ("source_type", AL_SOURCE_TYPE),
                 ("looping", AL_LOOPING),
                 ("source_state", AL_SOURCE_STATE),
                 ("sample_offset", AL_SAMPLE_OFFSET),
                 ("byte_offset", AL_BYTE_OFFSET)
                 ]
        source = SoundSource()
        for v in vals:
            for name, dprop in props:
                source.changedproperties = []
                self.assertFalse(source.changed)
                setattr(source, name, v)
                self.assertEqual(getattr(source, name), v)
                self.assertEqual(source.dataproperties[dprop], v)
                self.assertTrue(source.changed)
                self.assertTrue(dprop in source.changedproperties)

    def test_SoundSink(self):
        sink = SoundSink()
        self.assertIsNotNone(sink.device)
        self.assertIsNotNone(sink.context)
        self.assertTrue(sink.opened_device)
        #sink2 = SoundSink()
        #self.assertEqual(sink2.device, sink.device)
        del sink


if __name__ == "__main__":
    sys.exit(unittest.main())
