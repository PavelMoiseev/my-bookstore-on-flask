import datetime
from flask_login import current_user
from dotenv import load_dotenv
from .db_models import Order, Ordered_item, db, User


load_dotenv()


def fulfill_order(session):
	""" Fulfils order on successful payment """
	uid = session["uid"]
	order = Order(uid=uid, date=datetime.datetime.now(), status="processing")
	db.session.add(order)
	db.session.commit()

	current_user = User.query.get(uid)
	for cart in current_user.cart:
		ordered_item = Ordered_item(oid=order.id, itemid=cart.item.id, quantity=cart.quantity)
		db.session.add(ordered_item)
		db.session.commit()
		current_user.remove_from_cart(cart.item.id, cart.quantity)
		db.session.commit()

def admin_only(func):
	""" Decorator for giving access to authorized users only """
	def wrapper(*args, **kwargs):
		if current_user.is_authenticated and current_user.admin == 1:
			return func(*args, **kwargs)
		else:
			return "You are not Authorized to access this URL."
	wrapper.__name__ = func.__name__
	return wrapper
		