import os
from datetime import datetime
import logging
from flask import Flask, render_template, redirect, request, session, flash,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_bcrypt import Bcrypt  # Import Flask-Bcrypt
from wtforms import SelectField

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# User model
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.String(250), nullable=True)  # Add bio field
    emoji = db.Column(db.String(10), nullable=True)  # Add emoji field

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    emoji = SelectField('Choose Emoji',choices = [
    ('😀', '😀 Happy'),
    ('😃', '😃 Grinning Face with Big Eyes'),
    ('😄', '😄 Grinning Face with Smiling Eyes'),
    ('😁', '😁 Beaming Face with Smiling Eyes'),
    ('😆', '😆 Grinning Squinting Face'),
    ('😅', '😅 Grinning Face with Sweat'),
    ('😂', '😂 Face with Tears of Joy'),
    ('🤣', '🤣 Rolling on the Floor Laughing'),
    ('😜', '😜 Winking Face with Tongue'),
    ('😝', '😝 Squinting Face with Tongue'),
    ('😛', '😛 Face with Tongue'),
    ('🤑', '🤑 Money-Mouth Face'),
    ('🤗', '🤗 Hugging Face'),
    ('😎', '😎 Smiling Face with Sunglasses'),
    ('🤩', '🤩 Star-Struck'),
    ('🥳', '🥳 Party Face'),
    ('😏', '😏 Smirking Face'),
    ('😒', '😒 Unamused Face'),
    ('😞', '😞 Disappointed Face'),
    ('😔', '😔 Pensive Face'),
    ('😟', '😟 Worried Face'),
    ('😤', '😤 Face with Steam from Nose'),
    ('😠', '😠 Angry Face'),
    ('😡', '😡 Pouting Face'),
    ('🤬', '🤬 Face with Symbols on Mouth'),
    ('😱', '😱 Face Screaming in Fear'),
    ('😨', '😨 Fearful Face'),
    ('😰', '😰 Anxious Face with Sweat'),
    ('😥', '😥 Sad but Relieved Face'),
    ('😢', '😢 Crying Face'),
    ('😭', '😭 Loudly Crying Face'),
    ('😓', '😓 Downcast Face with Sweat'),
    ('😩', '😩 Weary Face'),
    ('😫', '😫 Tired Face'),
    ('🥺', '🥺 Pleading Face'),
    ('😤', '😤 Face with Steam from Nose'),
    ('😮', '😮 Face with Open Mouth'),
    ('😯', '😯 Hushed Face'),
    ('😲', '😲 Astonished Face'),
    ('😳', '😳 Flushed Face'),
    ('🥵', '🥵 Hot Face'),
    ('🥶', '🥶 Cold Face'),
    ('😵', '😵 Dizzy Face'),
    ('🤯', '🤯 Exploding Head'),
    ('😶', '😶 Face Without Mouth'),
    ('😏', '😏 Smirking Face'),
    ('😬', '😬 Grimacing Face'),
    ('🙄', '🙄 Face with Rolling Eyes'),
    ('🤥', '🤥 Lying Face'),
    ('😬', '😬 Grimacing Face'),
    ('😯', '😯 Hushed Face'),
    ('😶', '😶 Face Without Mouth'),
    ('😲', '😲 Astonished Face'),
    ('😳', '😳 Flushed Face'),
    ('🙈', '🙈 See-No-Evil Monkey'),
    ('🙉', '🙉 Hear-No-Evil Monkey'),
    ('🙊', '🙊 Speak-No-Evil Monkey'),
    ('💀', '💀 Skull'),
    ('👻', '👻 Ghost'),
    ('👽', '👽 Alien'),
    ('🤖', '🤖 Robot Face'),
    ('😺', '😺 Grinning Cat Face'),
    ('😸', '😸 Grinning Cat Face with Smiling Eyes'),
    ('😻', '😻 Smiling Cat Face with Heart-Eyes'),
    ('😼', '😼 Cat Face with Wry Smile'),
    ('😽', '😽 Kissing Cat Face'),
    ('🙀', '🙀 Weary Cat Face'),
    ('😿', '😿 Crying Cat Face'),
    ('😾', '😾 Pouting Cat Face'),
    ('💩', '💩 Pile of Poo'),
    ('😹', '😹 Cat Face with Tears of Joy'),
    ('😾', '😾 Pouting Cat'),
    ('🤬', '🤬 Face with Symbols on Mouth'),
    ('😺', '😺 Grinning Cat Face'),
    ('😸', '😸 Grinning Cat Face with Smiling Eyes'),
    ('😻', '😻 Smiling Cat Face with Heart-Eyes'),
    ('🙀', '🙀 Weary Cat Face'),
    ('😿', '😿 Crying Cat Face'),
    ('😾', '😾 Pouting Cat Face'),
    ('🌟', '🌟 Glowing Star'),
    ('✨', '✨ Sparkles'),
    ('🌈', '🌈 Rainbow'),
    ('🎉', '🎉 Party Popper'),
    ('🎈', '🎈 Balloon'),
    ('🎊', '🎊 Confetti Ball'),
    ('🎃', '🎃 Jack-O-Lantern'),
    ('🎆', '🎆 Fireworks'),
    ('🎇', '🎇 Sparkler'),
    ('🧨', '🧨 Firecracker'),
    ('🧊', '🧊 Ice Cube'),
    ('☃️', '☃️ Snowman'),
    ('🎄', '🎄 Christmas Tree'),
    ('🍀', '🍀 Four Leaf Clover'),
    ('🍉', '🍉 Watermelon'),
    ('🍕', '🍕 Pizza'),
    ('🍔', '🍔 Hamburger'),
    ('🌭', '🌭 Hot Dog'),
    ('🍟', '🍟 French Fries'),
    ('🍦', '🍦 Ice Cream'),
    ('🍩', '🍩 Doughnut'),
    ('🍪', '🍪 Cookie'),
    ('🥗', '🥗 Green Salad'),
    ('🍰', '🍰 Shortcake'),
    ('🍫', '🍫 Chocolate Bar'),
    ('🍬', '🍬 Candy'),
    ('🍭', '🍭 Lollipop'),
    ('🍯', '🍯 Honey Pot'),
    ('🥥', '🥥 Coconut'),
    ('🌽', '🌽 Ear of Corn'),
    ('🥩', '🥩 Cut of Meat'),
    ('🍳', '🍳 Cooking'),
    ('🍔', '🍔 Hamburger'),
    ('🍙', '🍙 Rice Ball'),
    ('🍚', '🍚 Cooked Rice'),
    ('🍘', '🍘 Rice Cracker'),
    ('🍥', '🍥 Fish Cake'),
    ('🍣', '🍣 Sushi'),
    ('🍤', '🍤 Shrimp'),
    ('🍱', '🍱 Bento Box'),
    ('🍛', '🍛 Curry Rice'),
    ('🍜', '🍜 Steaming Bowl'),
    ('🍲', '🍲 Pot of Food'),
    ('🍧', '🍧 Shaved Ice'),
    ('🍨', '🍨 Ice Cream'),
    ('🥧', '🥧 Pie'),
    ('🥮', '🥮 Moon Cake'),
    ('🍕', '🍕 Pizza'),
    ('🥙', '🥙 Stuffed Flatbread'),
    ('🥐', '🥐 Croissant'),
    ('🍖', '🍖 Meat on Bone'),
    ('🍗', '🍗 Poultry Leg'),
    ('🍠', '🍠 Sweet Potato'),
    ('🥔', '🥔 Potato'),
    ('🥕', '🥕 Carrot'),
    ('🌽', '🌽 Ear of Corn'),
    ('🌶️', '🌶️ Hot Pepper'),
    ('🥒', '🥒 Cucumber'),
    ('🥬', '🥬 Leafy Green'),
    ('🥦', '🥦 Broccoli'),
    ('🍆', '🍆 Eggplant'),
    ('🍅', '🍅 Tomato'),
    ('🧄', '🧄 Garlic'),
    ('🧅', '🧅 Onion'),
    ('🍊', '🍊 Tangerine'),
    ('🍋', '🍋 Lemon'),
    ('🍌', '🍌 Banana'),
    ('🍉', '🍉 Watermelon'),
    ('🍇', '🍇 Grapes'),
    ('🍓', '🍓 Strawberry'),
    ('🍒', '🍒 Cherries'),
    ('🍑', '🍑 Peach'),
    ('🥭', '🥭 Mango'),
    ('🍍', '🍍 Pineapple'),
    ('🥥', '🥥 Coconut'),
    ('🥝', '🥝 Kiwi Fruit'),
    ('🍏', '🍏 Green Apple'),
    ('🍎', '🍎 Red Apple'),
    ('🍐', '🍐 Pear'),
    ('🍑', '🍑 Peach'),
    ('🍊', '🍊 Orange'),
    ('🍋', '🍋 Lemon'),
    ('🍌', '🍌 Banana'),
    ('🍉', '🍉 Watermelon'),
    ('🍇', '🍇 Grapes'),
    ('🍓', '🍓 Strawberry'),
    ('🍒', '🍒 Cherries'),
    ('🍑', '🍑 Peach'),
    ('🍊', '🍊 Orange'),
    ('🍋', '🍋 Lemon'),
    ('🍌', '🍌 Banana'),
    ('🍉', '🍉 Watermelon'),
    ('🍇', '🍇 Grapes'),
    ('🍓', '🍓 Strawberry'),
    ('🍒', '🍒 Cherries'),
    ('🍑', '🍑 Peach'),
    ('🍊', '🍊 Orange'),
    ('🍋', '🍋 Lemon'),
    ('🍌', '🍌 Banana'),
    ('🍉', '🍉 Watermelon'),
    ('🍇', '🍇 Grapes'),
    ('🍓', '🍓 Strawberry'),
    ('🍒', '🍒 Cherries'),
    ('🍑', '🍑 Peach'),
    ('🍊', '🍊 Orange'),
    ('🍋', '🍋 Lemon'),
    ('🍌', '🍌 Banana'),
    ('🍉', '🍉 Watermelon'),
    ('🍇', '🍇 Grapes'),
    ('🍓', '🍓 Strawberry'),
    ('🍒', '🍒 Cherries'),
    ('🍑', '🍑 Peach'),
    ('🥭', '🥭 Mango'),
    ('🍍', '🍍 Pineapple'),
    ('🌰', '🌰 Chestnut'),
    ('🌾', '🌾 Sheaf of Rice'),
    ('🌿', '🌿 Herb'),
    ('🌱', '🌱 Seedling'),
    ('🍀', '🍀 Four Leaf Clover'),
    ('🌷', '🌷 Tulip'),
    ('🌼', '🌼 Blossom'),
    ('🌸', '🌸 Cherry Blossom'),
    ('💐', '💐 Bouquet'),
    ('🌻', '🌻 Sunflower'),
    ('🌺', '🌺 Hibiscus'),
    ('🍃', '🍃 Leaf Fluttering in Wind'),
    ('🍂', '🍂 Fallen Leaf'),
    ('🍁', '🍁 Maple Leaf'),
    ('🌈', '🌈 Rainbow'),
    ('☀️', '☀️ Sun'),
    ('🌤️', '🌤️ Sun Behind Small Cloud'),
    ('⛅', '⛅ Sun Behind Cloud'),
    ('🌥️', '🌥️ Sun Behind Large Cloud'),
    ('🌦️', '🌦️ Sun Behind Rain Cloud'),
    ('🌧️', '🌧️ Cloud with Rain'),
    ('🌨️', '🌨️ Cloud with Snow'),
    ('🌩️', '🌩️ Cloud with Lightning'),
    ('🌪️', '🌪️ Tornado'),
    ('🌫️', '🌫️ Fog'),
    ('🌬️', '🌬️ Wind Face'),
    ('🌊', '🌊 Water Wave'),
    ('💧', '💧 Droplet'),
    ('💦', '💦 Sweat Droplets'),
    ('🌌', '🌌 Milky Way'),
    ('🌠', '🌠 Shooting Star'),
    ('⭐', '⭐ Star'),
    ('🌟', '🌟 Glowing Star'),
    ('⚡', '⚡ High Voltage'),
    ('🔥', '🔥 Fire'),
    ('💥', '💥 Collision'),
    ('🌈', '🌈 Rainbow'),
    ('❄️', '❄️ Snowflake'),
    ('☔', '☔ Umbrella with Rain Drops'),
    ('🌞', '🌞 Sun with Face'),
    ('🌜', '🌜 Crescent Moon Face'),
    ('🌛', '🌛 First Quarter Moon Face'),
    ('🌙', '🌙 Crescent Moon'),
    ('🌚', '🌚 New Moon Face'),
    ('🌑', '🌑 New Moon'),
    ('🌓', '🌓 First Quarter Moon'),
    ('🌔', '🌔 Waxing Gibbous Moon'),
    ('🌕', '🌕 Full Moon'),
    ('🌖', '🌖 Waning Gibbous Moon'),
    ('🌗', '🌗 Last Quarter Moon'),
    ('🌘', '🌘 Waning Crescent Moon'),
    ('🌍', '🌍 Earth Globe Europe-Africa'),
    ('🌎', '🌎 Earth Globe Americas'),
    ('🌏', '🌏 Earth Globe Asia-Australia'),
    ('🪐', '🪐 Ringed Planet'),
    ('🔭', '🔭 Telescope'),
    ('🧭', '🧭 Compass'),
    ('⛵', '⛵ Sailboat'),
    ('🛶', '🛶 Canoe'),
    ('🚤', '🚤 Speedboat'),
    ('🛳️', '🛳️ Passenger Ship'),
    ('🚢', '🚢 Cruise Ship'),
    ('🛥️', '🛥️ Motor Boat'),
    ('🛴', '🛴 Kick Scooter'),
    ('🛵', '🛵 Motor Scooter'),
    ('🚲', '🚲 Bicycle'),
    ('🚜', '🚜 Tractor'),
    ('🚗', '🚗 Automobile'),
    ('🚙', '🚙 SUV'),
    ('🚌', '🚌 Bus'),
    ('🚍', '🚍 Oncoming Bus'),
    ('🚎', '🚎 Trolleybus'),
    ('🚏', '🚏 Bus Stop'),
    ('🏍️', '🏍️ Motorcycle'),
    ('🛵', '🛵 Motor Scooter'),
    ('🚨', '🚨 Police Car Light'),
    ('🚔', '🚔 Police Car'),
    ('🚕', '🚕 Taxi'),
    ('🚖', '🚖 Oncoming Taxi'),
    ('🚘', '🚘 Oncoming Automobile'),
    ('🚙', '🚙 Oncoming SUV'),
    ('🚌', '🚌 Oncoming Bus'),
    ('🚎', '🚎 Oncoming Trolleybus'),
    ('🚏', '🚏 Bus Stop'),
    ('⛽', '⛽ Fuel Pump'),
    ('🛣️', '🛣️ Motorway'),
    ('🛤️', '🛤️ Railway Track'),
    ('🚥', '🚥 Traffic Light'),
    ('🚦', '🚦 Vertical Traffic Light'),
    ('🚧', '🚧 Construction'),
    ('🔧', '🔧 Wrench'),
    ('🔨', '🔨 Hammer'),
    ('⚒️', '⚒️ Hammer and Pick'),
    ('🪚', '🪚 Handsaw'),
    ('🔩', '🔩 Nut and Bolt'),
    ('⚙️', '⚙️ Gear'),
    ('🧰', '🧰 Toolbox'),
    ('🔋', '🔋 Battery'),
    ('🔌', '🔌 Electric Plug'),
    ('💻', '💻 Laptop'),
    ('🖥️', '🖥️ Desktop Computer'),
    ('🖨️', '🖨️ Printer'),
    ('🖱️', '🖱️ Computer Mouse'),
    ('🖊️', '🖊️ Pen'),
    ('🖋️', '🖋️ Fountain Pen'),
    ('✏️', '✏️ Pencil'),
    ('📝', '📝 Memo'),
    ('📁', '📁 File Folder'),
    ('📂', '📂 Open File Folder'),
    ('📅', '📅 Calendar'),
    ('📆', '📆 Tear-Off Calendar'),
    ('📇', '📇 Card Index'),
    ('🗂️', '🗂️ Card Index Dividers'),
    ('🗃️', '🗃️ Card File Box'),
    ('🗄️', '🗄️ File Cabinet'),
    ('🗑️', '🗑️ Wastebasket'),
    ('🧾', '🧾 Receipt'),
    ('📜', '📜 Scroll'),
    ('📃', '📃 Page with Curl'),
    ('📋', '📋 Clipboard'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📅', '📅 Calendar'),
    ('📆', '📆 Tear-Off Calendar'),
    ('🗒️', '🗒️ Spiral Notepad'),
    ('📕', '📕 Closed Book'),
    ('📗', '📗 Green Book'),
    ('📘', '📘 Blue Book'),
    ('📙', '📙 Orange Book'),
    ('📓', '📓 Notebook'),
    ('📔', '📔 Notebook with Decorative Cover'),
    ('📚', '📚 Books'),
    ('🔖', '🔖 Bookmark'),
    ('🏷️', '🏷️ Label'),
    ('💼', '💼 Briefcase'),
    ('📦', '📦 Package'),
    ('📬', '📬 Incoming Envelope'),
    ('📭', '📭 Inbox Tray'),
    ('📮', '📮 Postbox'),
    ('✉️', '✉️ Envelope'),
    ('📧', '📧 E-Mail'),
    ('📤', '📤 Outbox Tray'),
    ('📥', '📥 Inbox Tray'),
    ('📪', '📪 Empty Mailbox'),
    ('📫', '📫 Mailbox with Raised Flag'),
    ('📮', '📮 Postbox'),
    ('📯', '📯 Postal Horn'),
    ('📦', '📦 Package'),
    ('📬', '📬 Incoming Envelope'),
    ('📭', '📭 Inbox Tray'),
    ('📮', '📮 Postbox'),
    ('📤', '📤 Outbox Tray'),
    ('📥', '📥 Inbox Tray'),
    ('📪', '📪 Empty Mailbox'),
    ('📫', '📫 Mailbox with Raised Flag'),
    ('🔑', '🔑 Key'),
    ('🗝️', '🗝️ Old Key'),
    ('🔐', '🔐 Locked with Key'),
    ('🔒', '🔒 Locked'),
    ('🔓', '🔓 Unlocked'),
    ('🚪', '🚪 Door'),
    ('🪣', '🪣 Bucket'),
    ('🧳', '🧳 Luggage'),
    ('🔍', '🔍 Magnifying Glass Tilted Left'),
    ('🔎', '🔎 Magnifying Glass Tilted Right'),
    ('🔦', '🔦 Flashlight'),
    ('🧭', '🧭 Compass'),
    ('🧯', '🧯 Fire Extinguisher'),
    ('🛠️', '🛠️ Hammer and Wrench'),
    ('⚙️', '⚙️ Gear'),
    ('🛠️', '🛠️ Hammer and Wrench'),
    ('🔋', '🔋 Battery'),
    ('🔌', '🔌 Electric Plug'),
    ('🧰', '🧰 Toolbox'),
    ('🔒', '🔒 Locked'),
    ('🔓', '🔓 Unlocked'),
    ('🔑', '🔑 Key'),
    ('🗝️', '🗝️ Old Key'),
    ('🔐', '🔐 Locked with Key'),
    ('🧴', '🧴 Lotion Bottle'),
    ('🧴', '🧴 Lotion Bottle'),
    ('🧷', '🧷 Safety Pin'),
    ('🧹', '🧹 Broom'),
    ('🧺', '🧺 Basket'),
    ('🧼', '🧼 Soap'),
    ('🧽', '🧽 Sponge'),
    ('🧴', '🧴 Lotion Bottle'),
    ('🧷', '🧷 Safety Pin'),
    ('🧹', '🧹 Broom'),
    ('🧺', '🧺 Basket'),
    ('🧼', '🧼 Soap'),
    ('🧽', '🧽 Sponge'),
    ('🧹', '🧹 Broom'),
    ('🧺', '🧺 Basket'),
    ('🧼', '🧼 Soap'),
    ('🧽', '🧽 Sponge'),
    ('🧴', '🧴 Lotion Bottle'),
    ('🧷', '🧷 Safety Pin'),
    ('🧹', '🧹 Broom'),
    ('🧺', '🧺 Basket'),
    ('🧼', '🧼 Soap'),
    ('🧽', '🧽 Sponge'),
    ('🔑', '🔑 Key'),
    ('🔒', '🔒 Locked'),
    ('🔓', '🔓 Unlocked'),
    ('🔐', '🔐 Locked with Key'),
    ('🔑', '🔑 Key'),
    ('🔒', '🔒 Locked'),
    ('🔓', '🔓 Unlocked'),
    ('🔐', '🔐 Locked with Key'),
    ('💡', '💡 Light Bulb'),
    ('🔦', '🔦 Flashlight'),
    ('📦', '📦 Package'),
    ('🗂️', '🗂️ Card Index Dividers'),
    ('🗄️', '🗄️ File Cabinet'),
    ('📑', '📑 Bookmark Tabs'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
    ('📊', '📊 Bar Chart'),
    ('📈', '📈 Chart Increasing'),
    ('📉', '📉 Chart Decreasing'),
]
)
    submit = SubmitField('Register')
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Like model
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Upload')

with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect('/login')
    
    post = Post.query.get_or_404(post_id)
    comment_text = request.form.get('comment')
    
    if comment_text:
        new_comment = Comment(post_id=post.id, username=session['username'], text=comment_text)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        logging.info(f'User {session["username"]} commented on post {post.id}.')
    else:
        flash('Comment cannot be empty.', 'danger')

    return redirect('/feeds')
@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect('/login')

    post = Post.query.get_or_404(post_id)
    user_liked = Like.query.filter_by(post_id=post.id, username=session['username']).first()

    if not user_liked:
        new_like = Like(post_id=post.id, username=session['username'])
        db.session.add(new_like)
        db.session.commit()
        flash('You liked this post!', 'success')
        logging.info(f'User {session["username"]} liked post {post.id}.')
    else:
        flash('You have already liked this post!', 'warning')

    return redirect('/feeds')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        emoji = form.emoji.data  # Get selected emoji

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return render_template('register.html', form=form)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Use bcrypt
        new_user = User(username=username, password=hashed_password, bio="", emoji=emoji) 
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        logging.info(f'New user registered: {username}')
        return redirect('/login')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):  # Use Flask-Bcrypt
            session['username'] = username
            logging.info(f'User logged in: {username}')
            return redirect('/feeds')
        else:
            flash('Login failed! Check your username and password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect('/login')

    form = PostForm()
    if form.validate_on_submit():
        content = form.content.data
        new_post = Post(username=session['username'], content=content)
        db.session.add(new_post)
        db.session.commit()
        flash('Post uploaded successfully!', 'success')
        logging.info(f'User {session["username"]} uploaded a post.')
        return redirect('/feeds')

    return render_template('upload.html', form=form)

@app.route('/feeds')
def feeds():
    posts = Post.query.all()
    # Get emojis for each user from the database
    user_emojis = {user.username: user.emoji for user in User.query.all()}  
    return render_template('feeds.html', posts=posts, user_emojis=user_emojis)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect('/login')

    post = Post.query.get_or_404(post_id)
    if post.username == session['username']:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        logging.info(f'User {session["username"]} deleted a post.')
    else:
        flash('You do not have permission to delete this post.', 'danger')

    return redirect('/feeds')

@app.route('/logout')
def logout():
    logging.info(f'User logged out: {session["username"]}')
    session.pop('username', None)
    return redirect('/')
@app.route('/profile/')
def profile():
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect('/login')
    
    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        flash('User not found!', 'danger')
        return redirect('/')
    
    # Fetch user details
    user_emoji = user.emoji if user and hasattr(user, 'emoji') else "😊"  # Default emoji if not found
    user_bio = user.bio if user and hasattr(user, 'bio') else "This user has no bio."

    # Get user posts
    posts = Post.query.filter_by(username=username).all()
    
    return render_template('profile.html', user=user, posts=posts, user_emoji=user_emoji, user_bio=user_bio, profile_link=url_for('user_profile', username=username))

@app.route('/profile/<username>')
def user_profile(username):
    # Query the user by username
    user = User.query.filter_by(username=username).first()

    if user is None:
        # If the user doesn't exist, show an error message and redirect to the home page
        flash('User not found!', 'danger')
        return redirect('/')

    # Fetch the user's posts
    user_posts = Post.query.filter_by(username=user.username).all()

    # Fetch user emoji and bio from the user object
    user_emoji = user.emoji
    user_bio = user.bio

    return render_template('profile.html', user=user, posts=user_posts, post_count=len(user_posts), user_emoji=user_emoji, user_bio=user_bio, profile_link=url_for('user_profile', username=username))

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        flash('You need to log in first!', 'warning')
        return redirect('/login')

    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    if request.method == 'POST':
        # Update user information
        user.bio = request.form.get('bio', user.bio)  # Get bio from form, use existing if not provided
        user.emoji = request.form.get('emoji', user.emoji)  # Get emoji from form, use existing if not provided
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect('/profile')

    # Pre-fill the form with current user data
    return render_template('edit_profile.html', user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
