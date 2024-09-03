from flask import Blueprint, render_template, session, flash
from flask_login import login_required
from .models import User
from datetime import datetime

# this can be removed when the create listing function is moved back to items.py
from .models import Item, Comment, Bid, Watchlist
from .forms import ItemForm, CommentForm
from .items import check_upload_file
from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('main', __name__)


## Index/Home page route
@bp.route('/')
def index():
    items = Item.query.all()
    datetime_now = datetime.now()

    bids = Bid.query.all()
    watchlist = Watchlist.query.all()


    #num bids for each item
    numBidsDict = {}

    for i in range(len(items)):
        numBids = 0
        for bid in bids:
            if (items[i].id == bid.item_id):
                numBids = numBids + 1
        numBidsDict[items[i].id] = numBids

    #num watching for each item
    numWatchDict = {}

    for i in range(len(items)):
        numWatch = 0
        for watch in watchlist:
            if (items[i].id == watch.item_id):
                numWatch = numWatch + 1
        numWatchDict[items[i].id] = numWatch

    top_items = sorted(numBidsDict, key=numBidsDict.get, reverse=True)

    return render_template('landing.html', numWatchDict=numWatchDict, numBidsDict=numBidsDict, items=items,  top_items=top_items, bids=bids, datetime_now=datetime_now)

## For text search 
@bp.route('/search')
def search():
    datetime_now = datetime.now()  
    search_term = request.values.get('search_term')

    if search_term:
        results = Item.query.filter(Item.title.like(f'%{search_term}%')).all()
        
        bids = Bid.query.all()
        watchlist = Watchlist.query.all()

        #num bids for each item
        numBidsDict = {}

        for i in range(len(results)):
            numBids = 0
            for bid in bids:
                if (results[i].id == bid.item_id):
                    numBids = numBids + 1
            numBidsDict[results[i].id] = numBids

        #num watching for each item
        numWatchDict = {}

        for i in range(len(results)):
            numWatch = 0
            for watch in watchlist:
                if (results[i].id == watch.item_id):
                    numWatch = numWatch + 1
            numWatchDict[results[i].id] = numWatch

        return render_template('landing.html', search_term=search_term, results=results, numWatchDict=numWatchDict, numBidsDict=numBidsDict, bids=bids, datetime_now=datetime_now)
    else:
        return redirect(url_for('main.index'))

## Search for games with a particular genre
@bp.route('/genre')
def genre():
    datetime_now = datetime.now()
   
    search_term = request.values.get('search_term')

    if search_term:
        results = Item.query.filter(Item.genre.like(search_term)).all()
        
        bids = Bid.query.all()
        watchlist = Watchlist.query.all()

        #num bids for each item
        numBidsDict = {}

        for i in range(len(results)):
            numBids = 0
            for bid in bids:
                if (results[i].id == bid.item_id):
                    numBids = numBids + 1
            numBidsDict[results[i].id] = numBids

        #num watching for each item
        numWatchDict = {}

        for i in range(len(results)):
            numWatch = 0
            for watch in watchlist:
                if (results[i].id == watch.item_id):
                    numWatch = numWatch + 1
            numWatchDict[results[i].id] = numWatch

        return render_template('landing.html', search_term=search_term, results=results, numWatchDict=numWatchDict, numBidsDict=numBidsDict, bids=bids, datetime_now=datetime_now)
    else:
        return redirect(url_for('main.index'))

## Search for games with a particular platform
@bp.route('/platform')
def platform():
    datetime_now = datetime.now()

    bids = Bid.query.all()
    watchers = Watchlist.query.all()
    
    search_term = request.values.get('search_term')

    if search_term:
        results = Item.query.filter(Item.platform.like(search_term)).all()
        bids = Bid.query.all()
        watchlist = Watchlist.query.all()

        #num bids for each item
        numBidsDict = {}

        for i in range(len(results)):
            numBids = 0
            for bid in bids:
                if (results[i].id == bid.item_id):
                    numBids = numBids + 1
            numBidsDict[results[i].id] = numBids

        #num watching for each item
        numWatchDict = {}

        for i in range(len(results)):
            numWatch = 0
            for watch in watchlist:
                if (results[i].id == watch.item_id):
                    numWatch = numWatch + 1
            numWatchDict[results[i].id] = numWatch

        return render_template('landing.html', search_term=search_term, results=results, numWatchDict=numWatchDict, numBidsDict=numBidsDict, bids=bids, datetime_now=datetime_now)
    else:
        return redirect(url_for('main.index'))

## Search for games with a particular release year
@bp.route('/year')
def year():
    datetime_now = datetime.now()

    bids = Bid.query.all()
    watchers = Watchlist.query.all()
    
    search_term = request.values.get('search_term')

    if search_term:
        results = Item.query.filter(Item.release_year.like(search_term)).all()
        bids = Bid.query.all()
        watchlist = Watchlist.query.all()

        #num bids for each item
        numBidsDict = {}

        for i in range(len(results)):
            numBids = 0
            for bid in bids:
                if (results[i].id == bid.item_id):
                    numBids = numBids + 1
            numBidsDict[results[i].id] = numBids

        #num watching for each item
        numWatchDict = {}

        for i in range(len(results)):
            numWatch = 0
            for watch in watchlist:
                if (results[i].id == watch.item_id):
                    numWatch = numWatch + 1
            numWatchDict[results[i].id] = numWatch

        return render_template('landing.html', search_term=search_term, results=results, numWatchDict=numWatchDict, numBidsDict=numBidsDict, bids=bids, datetime_now=datetime_now)
    else:
        return redirect(url_for('main.index'))

## Watchlist
@bp.route('/watchlist')
@login_required
def watchlist():

    #get user information from db
    user_name = session.get("user_name")
    user = User.query.filter(User.user_name==user_name).first()

    #get watchlist items associated with user
    items = Watchlist.query.filter(Watchlist.user_id==user.id).all()

    # Get bid info
    bids = Bid.query.all()

    #num bids for each item
    numBidsDict = {}
            
    for i in range(len(items)):
        numBids = 0
        for bid in bids:
            if (items[i].item.id == bid.item_id):
                numBids = numBids + 1
        numBidsDict[items[i].id] = numBids 

    return render_template('watchlist.html', items=items, numBidsDict=numBidsDict)

## 404 Error Handler
@bp.app_errorhandler(404)
def error404(error):
    return render_template('errors/404.html'), 404

## 500 Error Handler
@bp.app_errorhandler(500)
def error500(error):
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(Exception)
def catchAllError(error):
    return render_template('errors/catchall.html')