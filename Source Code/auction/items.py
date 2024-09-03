from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Item, Comment, Bid, Watchlist, User
from .forms import ItemForm, CommentForm, PlaceBidForm, CloseAuctionForm, OpenAuctionForm, WatchForm
from . import db
from flask_login import login_required, current_user


#for file upload
import os
from werkzeug.utils import secure_filename


# create a blueprint
bp = Blueprint('item', __name__, url_prefix='/items')


# create a page that will show the details for the item
@bp.route('/<id>')
def show(id):
    item = Item.query.filter_by(id=id).first()
    
    watching = False

    if current_user.is_authenticated:
        watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()    

        for listing in watchlist:
            if listing.item_id == item.id:
                watching = True
            else:
                watching = False

    users = User.query.all()
    bidForm = PlaceBidForm()
    commentForm = CommentForm()
    closeForm = CloseAuctionForm()
    openForm = OpenAuctionForm()
    watchForm = WatchForm()
    return render_template('itemdetails.html', users=users, item=item, watching=watching,
                            form1=bidForm, form2=commentForm, form3=closeForm, form4=openForm, form5=watchForm)


# place bid
@bp.route('/<id>/bid', methods = ['GET', 'POST'])
@login_required
def place_bid(id):
    form = PlaceBidForm()
    item_obj = Item.query.filter_by(id=id).first()

    temp = form.bid.data

    if form.validate_on_submit():
        if temp > item_obj.current_bid:
            bid = Bid(bid_amount=form.bid.data,
                    item=item_obj,
                    user_id=current_user.id)
            item_obj.current_bid = form.bid.data
            db.session.add(bid) 
            db.session.commit()
            flash('Bid has been placed!', 'info')
        else:
            flash('Invalid bid amount: $' + str(form.bid.data) + '. Must be greater than current bid.', 'danger')

    return redirect(url_for('item.show', id=id))


# comment
@bp.route('/<id>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm() 
    item_obj = Item.query.filter_by(id=id).first()  
    if form.validate_on_submit():
        comment = Comment(text=form.text.data,  
                          item=item_obj,
                          user=current_user)
                    
        db.session.add(comment) 
        db.session.commit()
        print("Comment posted by the user:", form.text.data) 

    return redirect(url_for('item.show', id=id))


# watch item
@bp.route('/<id>/watch', methods = ['GET', 'POST'])
@login_required
def watch(id):
    form = WatchForm()
    item_obj = Item.query.filter_by(id=id).first()

    if form.validate_on_submit():
        item = Watchlist(item=item_obj,
                         user=current_user)
        db.session.add(item)
        db.session.commit()
        print("Item was added to watchlist") 
    
    return redirect(url_for('item.show', id=id))


# close auction
@bp.route('/<id>/close', methods = ['GET', 'POST'])
@login_required
def close_auction(id):
    form = CloseAuctionForm()
    item = Item.query.filter_by(id=id).first()

    if form.validate_on_submit():
        item.is_active = 0 
        db.session.commit()
        print("Auction was been closed") 
    
    return redirect(url_for('item.show', id=id))


# open auction
@bp.route('/<id>/open', methods = ['GET', 'POST'])
@login_required
def open_auction(id):
    form = OpenAuctionForm()
    item = Item.query.filter_by(id=id).first()

    if form.validate_on_submit():
        item.is_active = 1 
        db.session.commit()
        print("Auction was been opened") 
    
    return redirect(url_for('item.show', id=id))

# create item 
@bp.route('/list-item', methods=['GET','POST'])
@login_required
def create():
    form = ItemForm()

    if form.validate_on_submit():
        
        db_file_path = check_upload_file(form)
        
        # if the form was successfully submitted, access form data
        item = Item(title=form.title.data, 
                    description=form.description.data,
                    image=db_file_path,
                    genre=form.genre.data,
                    platform=form.platform.data,
                    classification=form.classification.data,
                    release_year=form.release_year.data,
                    starting_bid=form.starting_bid.data,
                    current_bid=form.starting_bid.data,
                    user=current_user)

        # add the object to the db session and commit
        db.session.add(item)
        db.session.commit()

        flash('Successfully created new listing','success')
        return redirect(url_for('item.create'))      
        
    return render_template('newlisting.html', form=form)


def check_upload_file(form):
    #get file data from form
    fp = form.image.data
    filename = fp.filename
    #get the current path of the module file... store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    #upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH,'static/img',secure_filename(filename))
    #store relative path in DB as image location in HTML is relative
    db_upload_path='/static/img/'+secure_filename(filename)
    #save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path





