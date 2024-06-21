import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Set the GST_PLUGIN_PATH environment variable
os.environ['GST_PLUGIN_PATH'] = '/usr/lib/x86_64-linux-gnu/gstreamer-1.0/'

def on_message(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-of-stream")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, {debug}")
        loop.quit()
    return True

Gst.init(None)

pipeline_str = """
    mvsrc ! videoconvert ! autovideosink
"""

pipeline = Gst.parse_launch(pipeline_str)
bus = pipeline.get_bus()
bus.add_signal_watch()
loop = GLib.MainLoop()

bus.connect("message", on_message, loop)
pipeline.set_state(Gst.State.PLAYING)

try:
    loop.run()
except Exception as e:
    print("Exception occurred:", e)
finally:
    pipeline.set_state(Gst.State.NULL)
