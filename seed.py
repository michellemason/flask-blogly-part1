from models import User, Tag, db 
from app import app

db.drop_all()
db.create_all()

mich = User(first_name='Michelle', last_name='Mason', image_url='https://static.vecteezy.com/system/resources/thumbnails/001/991/683/small/crown-isolated-icon-symbol-illustration-of-crown-icon-on-white-background-free-vector.jpg')
jake = User(first_name='Jake', last_name='Korinko', image_url='https://i.etsystatic.com/27152142/r/il/5c1415/3021507188/il_340x270.3021507188_r8ss.jpg')
walnut = User(first_name='Walnut', last_name='Masinko', image_url='https://icon-library.com/images/small-dog-icon/small-dog-icon-25.jpg')
fergie = User(first_name='Fergie', last_name='Idrovo')

db.session.add(mich)
db.session.add(jake)
db.session.add(walnut)
db.session.add(fergie)
db.session.commit()

fun = Tag(name='Fun')
zwonky = Tag(name='zwonky')
boop = Tag(name='Boop')
beep = Tag(name='Beep')

db.session.add(fun)
db.session.add(zwonky)
db.session.add(boop)
db.session.add(beep)
db.session.commit()