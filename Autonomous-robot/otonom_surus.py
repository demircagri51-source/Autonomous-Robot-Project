#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile

class OtonomSurus(Node):
    def __init__(self):
        super().__init__('otonom_gezgin')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscriber = self.create_subscription(
            LaserScan, 
            '/scan', 
            self.laser_callback, 
            QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.timer = self.create_timer(0.5, self.hareket_et)
        self.move_cmd = Twist()
        self.engel_var = False
        self.get_logger().info('Otonom Sürüş Başlatıldı! Robot gezmeye başlıyor...')

    def laser_callback(self, msg):
        # Lidar verisinin ön kısmını (0 derece ve çevresi) kontrol et
        # Waffle Pi için scan array yapısı bazen farklı olabilir, geniş bir açıya bakıyoruz.
        # Ön taraftaki 20 derecelik açıyı tarıyoruz.
        on_taraf = msg.ranges[0:20] + msg.ranges[-20:]
        
        min_mesafe = 10.0
        for mesafe in on_taraf:
            if 0.1 < mesafe < min_mesafe: # 0.1 hatalı verileri elemek için
                min_mesafe = mesafe

        # Eğer 0.6 metreden yakında engel varsa DUR ve DÖN
        if min_mesafe < 0.6:
            self.engel_var = True
        else:
            self.engel_var = False

    def hareket_et(self):
        if self.engel_var:
            # Engel var! Sola dön
            self.move_cmd.linear.x = 0.0
            self.move_cmd.angular.z = 0.5 # Dönme hızı
            self.get_logger().info('Engel algılandı! Dönülüyor...')
        else:
            # Yol temiz, ileri git
            self.move_cmd.linear.x = 0.2 # İlerleme hızı
            self.move_cmd.angular.z = 0.0
            self.get_logger().info('Yol temiz. İlerliyor...')
        
        self.publisher_.publish(self.move_cmd)

def main(args=None):
    rclpy.init(args=args)
    node = OtonomSurus()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Durdurulunca robotu durdur
        node.move_cmd.linear.x = 0.0
        node.move_cmd.angular.z = 0.0
        node.publisher_.publish(node.move_cmd)
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
