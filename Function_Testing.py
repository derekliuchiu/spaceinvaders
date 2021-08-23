import second_version
import unittest




# Testing edge_check()
# edge_check function checks if any of the enemies are touching the edge of the screen, if they are, delta is increased
# and speed is negative so the aliens can move backwards toward the other edge of the screen
# when enemies are drawn, their y position is enemy.y + delta, so by increasing delta it moves them down the screen

class TestGame(unittest.TestCase):

	# first check, enemy 2 is at x-position 1170, its width is 40, and width of the screen is 1200, so next frame it will touch the right edge
	# thus delta should increase, and speed should be negative
	def test_edge_check_1(self):
		second_version.delta = 0
		second_version.Alien_speed = 1

		test_list = []
		en1 = second_version.Alien(50, 40)
		en2 = second_version.Alien(1170, 40)
		test_list.append(en1)
		test_list.append(en2)
		second_version.edge_check(second_version.WIDTH, test_list)


		self.assertEqual(second_version.delta, 20)
		self.assertEqual(second_version.Alien_speed, -1)

	# second check, enemy 2 + its width + its speed is less than the width, meaning that next frame it will not touch the edge of the screen
	# thus delta and speed should stay the same
	def test_edge_check_2(self):
		second_version.delta = 0
		second_version.Alien_speed = 1

		test_list = []
		en1 = second_version.Alien(500, 600)
		en2 = second_version.Alien(1120, 40)
		test_list.append(en1)
		test_list.append(en2)
		second_version.edge_check(second_version.WIDTH, test_list)

		self.assertEqual(second_version.delta, 0)
		self.assertEqual(second_version.Alien_speed, 1)

	# third check, Alien.speed = -1 since enemy has bounced off right edge and is now traveling right to left
	# enemy x-position plus speed will equal 0 exactly, and thus will be touching the left edge of the screen
	# delta should change and speed should become -(-1) == 1
	def test_edge_check_3(self):
		second_version.delta = 0
		second_version.Alien_speed = -1

		test_list = []
		en1 = second_version.Alien(500, 520)
		en2 = second_version.Alien(1, 40)
		test_list.append(en1)
		test_list.append(en2)
		second_version.edge_check(second_version.WIDTH, test_list)

		self.assertEqual(second_version.delta, 20)
		self.assertEqual(second_version.Alien_speed, 1)



if __name__ == '__main__':
	unittest.main()

