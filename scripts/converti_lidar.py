import sys
import numpy as np
import rosbag2_py
from rclpy.serialization import deserialize_message, serialize_message
from sensor_msgs.msg import PointCloud2, PointField

TOPIC = '/rslidar_points'
NP = {1: 'i1', 2: 'u1', 3: 'i2', 4: 'u2', 5: 'i4', 6: 'u4', 7: 'f4', 8: 'f8'}
src, dst = sys.argv[1], sys.argv[2]

reader = rosbag2_py.SequentialReader()
reader.open(rosbag2_py.StorageOptions(uri=src, storage_id='sqlite3'),
            rosbag2_py.ConverterOptions('cdr', 'cdr'))
writer = rosbag2_py.SequentialWriter()
writer.open(rosbag2_py.StorageOptions(uri=dst, storage_id='sqlite3'),
            rosbag2_py.ConverterOptions('cdr', 'cdr'))
for t in reader.get_all_topics_and_types():
    writer.create_topic(t)

OUT = np.dtype({'names': ['x', 'y', 'z', 'intensity', 'ring', 'time'],
                'formats': ['f4', 'f4', 'f4', 'f4', 'u2', 'f4'],
                'offsets': [0, 4, 8, 12, 16, 20], 'itemsize': 24})
FIELDS = [('x', 0, 7), ('y', 4, 7), ('z', 8, 7), ('intensity', 12, 7),
          ('ring', 16, 4), ('time', 20, 7)]
ring_max, t_max, n_scan, printed = 0, 0.0, 0, False

while reader.has_next():
    topic, data, ts = reader.read_next()
    if topic == TOPIC:
        m = deserialize_message(data, PointCloud2)
        if not printed:
            print('campi originali:', [(f.name, f.datatype) for f in m.fields])
            printed = True
        dt = np.dtype({'names': [f.name for f in m.fields],
                       'formats': [NP[f.datatype] for f in m.fields],
                       'offsets': [f.offset for f in m.fields],
                       'itemsize': m.point_step})
        n = m.width * m.height
        a = np.frombuffer(bytes(m.data), dtype=dt, count=n)
        t0 = m.header.stamp.sec + m.header.stamp.nanosec * 1e-9
        rel = np.clip(a['timestamp'] - t0, 0, None)
        out = np.zeros(n, dtype=OUT)
        for k in ('x', 'y', 'z', 'intensity', 'ring'):
            out[k] = a[k]
        out['time'] = rel
        ring_max = max(ring_max, int(a['ring'].max()))
        t_max = max(t_max, float(rel.max()))
        n_scan += 1
        o = PointCloud2()
        o.header = m.header
        o.height, o.width = m.height, m.width
        o.fields = [PointField(name=n_, offset=off, datatype=d, count=1) for n_, off, d in FIELDS]
        o.is_bigendian = False
        o.point_step = 24
        o.row_step = 24 * m.width
        o.is_dense = m.is_dense
        o.data = out.tobytes()
        data = serialize_message(o)
    writer.write(topic, data, ts)

print('scan:', n_scan, ' ring max:', ring_max, ' time max (s):', t_max)