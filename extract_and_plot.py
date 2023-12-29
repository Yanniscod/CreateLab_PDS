import sqlite3
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
import csv

import matplotlib.pyplot as plt

class BagFileParser():
    def __init__(self, bag_file):
        self.conn = sqlite3.connect(bag_file)
        self.cursor = self.conn.cursor()

        ## create a message type map
        topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
        self.topic_type = {name_of:type_of for id_of,name_of,type_of in topics_data}
        self.topic_id = {name_of:id_of for id_of,name_of,type_of in topics_data}
        self.topic_msg_message = {name_of:get_message(type_of) for id_of,name_of,type_of in topics_data}

    def __del__(self):
        self.conn.close()

    # Return [(timestamp0, message0), (timestamp1, message1), ...]
    def get_messages(self, topic_name):
        
        topic_id = self.topic_id[topic_name]
        # Get from the db
        rows = self.cursor.execute("SELECT timestamp, data FROM messages WHERE topic_id = {}".format(topic_id)).fetchall()
        # Deserialise all and timestamp them
        return [ (timestamp,deserialize_message(data, self.topic_msg_message[topic_name])) for timestamp,data in rows]

def save_csv(x_values, y_values, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Y'])
        writer.writerows(zip(x_values, y_values))

def get_positions(topic_name, parser):
    x = []
    y = []

    for i in range(len(parser.get_messages(topic_name))):
        trajectory = parser.get_messages(topic_name)[i][1] 
        x.append(trajectory.pose.pose.position.x)
        y.append(trajectory.pose.pose.position.y)

    return x, y

def get_positions_odom(topic_name, parser):
    x = []
    y = []

    for i in range(len(parser.get_messages(topic_name))):
        trajectory = parser.get_messages(topic_name)[i][1] 
        print(trajectory.pose.pose.position.x)
        x.append(trajectory.pose.position.x)
        y.append(trajectory.pose.position.y)

    return x, y

def print_pos(topic_name, parser):

    trajectory = parser.get_messages(topic_name)[i][1] 
    print(trajectory.pose.pose.position.x)

if __name__ == "__main__":

        bag_file = 'ekf_data_b2/ekf_data_b2_0.db3'

        parser = BagFileParser(bag_file)
        x_marv = []
        y_marv = []
        x_odometry = []
        y_odometry = []
        x_calib_dots = []
        y_recalib_dots = []
        x_recalib = []
        y_recalib = []

        # actual = parser.get_messages("/marv/pos")
        print('Getting marv/pos')
        x_marv, y_marv = get_positions("/marv/pos", parser)  
        print('Getting odometry/global')
        x_odometry, y_odometry = get_positions("/odometry/global", parser)
        print('Getting calibrated pos dots')
        x_calib_dots, y_calib_dots = get_positions("/calibrated_pos_dots", parser)
        print('Getting pos with recalibration')
        x_recalib, y_recalib = get_positions("/recalibrated_pos", parser)

        plt.plot(x_marv, y_marv, label='raw Marvelmind position')
        # plt.plot(x_wheel, y_wheel, label='/wheel/odom')
        plt.plot(x_odometry, y_odometry, label='EKF position')

        plt.title('Effect of the filtering on the EM position')
        plt.xlabel('X Pos [m]')
        plt.ylabel('Y Pos [m]')
        plt.legend()
        
        # Save data to CSV files
        save_csv(x_marv, y_marv, 'marv_pos_data_U.csv')
        # save_csv(x_wheel, y_wheel, 'wheel_odom_data_U.csv')
        save_csv(x_odometry, y_odometry, 'odometry_global_data_U.csv')
        save_csv(x_calib_dots, y_calib_dots, 'calibrated_pos_dots_data_U.csv')
        save_csv(x_recalib, y_recalib, 'recalibrated_pos_data_U.csv')

        plt.show()
