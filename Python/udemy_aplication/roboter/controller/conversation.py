# controllerを上から順にみていけば、何しているかがわかる。

from roboter.models import robot


def talk_about_restaurant():
    """Function to speak with robot"""
    restaurant_robot = robot.RestaurantRobot()
    restaurant_robot.hello()
    restaurant_robot.recommend_restaurant()
    restaurant_robot.ask_user_favorite()
    restaurant_robot.thank_you()
