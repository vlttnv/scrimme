import re
import requests
from scrimme import scrimme, oid, models, db, lm
from flask import render_template, g, redirect, session, json, current_app, url_for
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime as dt

steam_id_regex = re.compile('steamcommunity.com/openid/id/(.*?)$')

"""
    STEAM LOGIN START
"""

def get_steam_userinfo(steam_id):
    """
        Return player summaries of the user that has the steam_id.
        Example:
        {
            u'steamid': u'steamid',
            u'personaname': u'personaname',
            ...
        }
        See: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0002.29
    """

    api = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'
    params = {
        'key': current_app.config['STEAM_API_KEY'],
        'steamids': steam_id,
        'format': json
    }
    user_info = requests.get(url=api, params=params)
    user_info_json = user_info.json()

    return user_info_json['response']['players'][0] or {}

@scrimme.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = models.User.query.filter_by(id=session['user_id']).first()

@scrimme.route("/login")
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    else:
        return oid.try_login("http://steamcommunity.com/openid")

@scrimme.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(oid.get_next_url())


@oid.after_login
def new_user(resp):
    steam_id = steam_id_regex.search(resp.identity_url).group(1)
    try:
        g.user = models.User.query.filter_by(steam_id=steam_id).one()
        user_info = get_steam_userinfo(g.user.steam_id)
        login_user(g.user)
        return redirect(oid.get_next_url())
    except NoResultFound:
        g.user = models.User()
        steam_data = get_steam_userinfo(steam_id)
        g.user.steam_id = steam_id
        g.user.nickname = steam_data['personaname']
        g.user.avatar_url = steam_data['avatar']
        g.user.avatar_url_full = steam_data['avatarfull']
        g.user.join_date = dt.utcnow()
        g.user.last_online = dt.utcnow()
        db.session.add(g.user)
        db.session.commit()
        login_user(g.user)
        return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@lm.unauthorized_handler
def unauthorized():
    # TODO: flash
    return redirect(url_for('index'))
"""
    STEAM LOGIN END
"""


@scrimme.route('/home')
# @login_required
def home():
    return render_template('index.html')


@scrimme.route('/')
def index():
    return render_template('onboard.html')


@scrimme.route('/profile/<steam_id>')
@login_required
def profile(steam_id):
    try:
        u = models.User.query.filter_by(steam_id=steam_id).one()
        return render_template(
            'profile.html',
            u=u,
        )
    except NoResultFound:
        return "no", 404