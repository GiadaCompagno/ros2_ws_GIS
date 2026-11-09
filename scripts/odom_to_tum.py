import sys
import rosbag2_py
from rclpy.serialization import deserialize_message
from nav_msgs.msg import Odometry

src, dst = sys.argv[1], sys.argv[2]
r = rosbag2_py.SequentialReader()
r.open(rosbag2_py.StorageOptions(uri=src, storage_id='sqlite3'),
       rosbag2_py.ConverterOptions('cdr', 'cdr'))
n = 0
with open(dst, 'w') as f:
    while r.has_next():
        topic, data, _ = r.read_next()
        if topic != '/Odometry':
            continue
        m = deserialize_message(data, Odometry)
        t = m.header.stamp.sec + m.header.stamp.nanosec * 1e-9
        p, q = m.pose.pose.position, m.pose.pose.orientation
        f.write(f"{t:.9f} {p.x} {p.y} {p.z} {q.x} {q.y} {q.z} {q.w}\n")
        n += 1
print('pose scritte:', n)