import unittest
from unittest import mock
from ESCController import ESCController


class testController(unittest.TestCase):
    @mock.patch("ESCController.sys")
    @mock.patch("ESCController.pigpio")
    def test_initialization_of_class(self, mock_pi, mock_sys):

        E = ESCController(4)

        self.assertEqual(E.pin_number, 4)
        mock_pi.pi.assert_called_once()
        mock_sys.exit.assert_not_called()

    @mock.patch("ESCController.pigpio")
    def test_change_motor_speed(self, mock_pi):
        mock_api = mock_pi.pi.return_value
        mock_api.set_servo_pulsewidth = mock.Mock()

        E = ESCController(4)

        E.change_motor_speed(100)

        E.change_motor_speed(0)

        E.change_motor_speed(150)

        E.change_motor_speed(-20)

        calls = [
            mock.call(4, 2000.0),
            mock.call(4, 700.0),
            mock.call(4, 2000.0),
            mock.call(4, 700.0),
        ]
        mock_api.set_servo_pulsewidth.assert_has_calls(calls)

    @mock.patch("ESCController.pigpio")
    def test_destructor(self, mock_pi):
        mock_api = mock_pi.pi.return_value
        mock_api.set_servo_pulsewidth = mock.Mock()

        E = ESCController(4)

        del E
        mock_api.set_servo_pulsewidth.assert_called_once_with(4, 0)
