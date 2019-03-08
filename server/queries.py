from bottle import request, response
from bottle import route, hook
from bottle import post, get, put, delete
import os
from pathlib import Path
import json

import sqlite3
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','dbs','recipes.db')) # Should work on every OS
conn = sqlite3.connect(db_path)

def format_response(d):
    return json.dumps(d,indent = 4) + '\n'


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route('/',method ='OPTIONS')
@route('/<path:path>',method='OPTIONS')
def options_handler(path = None):
    return


@get('/ping')
def get_ping():
    response.content_type = 'application/json'
    response.status = 200
    return format_response({'data':'ping'})
@get('/recipes/all')
def list_recipes():
    response.content_type = 'application/json'
    response.status = 200
    c = conn.cursor()
    c.execute("SELECT * FROM recipes")
    s = [{'recipe_id':recipe_id,'ingredients':json.loads(ingredients),'directions':directions,'title':title,'recipe_url':recipe_url}
            for (recipe_id,ingredients,directions,title,recipe_url) in c]
    return format_response(s)
@get('/recipes/<recipe_id>')
def search_recipe(recipe_id):
    response.content_type = 'application/json'
    query = """
        SELECT *
        FROM recipes
        WHERE recipe_id=?
        """
    c = conn.cursor()
    c.execute(query,[recipe_id])
    res = c.fetchone()
    print(res[0],res[1],res[2])
    s = {'recipe_id':res[0],'ingredients':json.loads(res[1]),'directions':res[2],'title':res[3],'recipe_url':res[4]}
    return format_response(s)

'''
@get('/movies/<imdb_id>')
def search_movie(imdb_id):
    response.content_type = 'application/json'
    query = """
        SELECT *
        FROM movies
        WHERE imdb_id=?
        """
    c = conn.cursor()
    c.execute(query,[imdb_id])
    s = [{"imdbKey": imdb_id, "title":title,"prod_year":prod_year}
        for (title,prod_year,imdb_id) in c]

    return format_response({'data':s})
'''
'''
Old stuff, kept for reference and examples.
@get('/movies')
def get_movies():
    response.content_type = 'application/json'
    title = request.query.title
    year = request.query.year
    if (title and year):
        c = conn.cursor()
        c.execute("""
            SELECT *
            FROM movies
            WHERE title=? AND prod_year=?
        """,[title,year])
        s = [{"imdbKey": imdb_id, "title":title,"prod_year":prod_year}
            for (title,prod_year,imdb_id) in c]
    else:
        query = """
            SELECT *
            FROM movies
            """
        c = conn.cursor()
        c.execute(query)
        s = [{"imdbKey": imdb_id, "title":title,"prod_year":prod_year}
            for (title,prod_year,imdb_id) in c]


    return format_response({'data':s})

@get('/movies/<imdb_id>')
def search_movie(imdb_id):
    response.content_type = 'application/json'
    query = """
        SELECT *
        FROM movies
        WHERE imdb_id=?
        """
    c = conn.cursor()
    c.execute(query,[imdb_id])
    s = [{"imdbKey": imdb_id, "title":title,"prod_year":prod_year}
        for (title,prod_year,imdb_id) in c]

    return format_response({'data':s})

@route('/reset',method=['GET','POST'])
def reset_database():
    c = conn.cursor()
    c.execute("DELETE FROM users")
    c.execute("DELETE FROM movies")
    c.execute("DELETE FROM performances")
    c.execute("DELETE FROM tickets")
    c.execute("DELETE FROM theaters")

    c.execute("""
    INSERT 
    INTO users(username,u_name,password)
    VALUES  ('alice','Alice','dobido'),
            ('bob','Bob','whasinaname')
    """)
    conn.commit()
    c.execute("""
    INSERT INTO movies(title,prod_year,imdb_id)
    VALUES  ('The Shape of Water', 2017, 'tt5580390'),
            ('Moonlight', 2016, 'tt4975722'),
            ('Spotlight', 2015, 'tt1895587'),
            ('Birdman', 2014, 'tt2562232')
    """)
    conn.commit()
    c.execute("""
    INSERT INTO theaters(t_name,capacity)
    VALUES  ('Kino', 10),
            ('Södran', 16),
            ('Skandia', 100)
    """)
    conn.commit()
    response.content_type = 'application/json'
    response.status = 200
    return format_response({"data":'OK'})

@route('/performances',method=['GET','POST'])
def add_performance():
    response.content_type = 'application/json'
    imdb_id = request.query.imdb
    theater = request.query.theater
    date = request.query.date
    time = request.query.time
    if (imdb_id and theater and date and time):
        c = conn.cursor()

        c.execute("SELECT imdb_id FROM movies WHERE imdb_id = ?",[imdb_id])
        movie_exist = list(c)
        c.execute("SELECT t_name FROM theaters WHERE t_name = ?",[theater])
        theater_exist = list(c)

        if(len(movie_exist) != 0 and len(theater_exist) != 0):
            query = """
                INSERT INTO performances(imdb_id,t_name,date,time)
                VALUES (?,?,?,?)
                """
            c.execute(query,[imdb_id,theater,date,time])
            conn.commit()
            p_id=c.execute("SELECT p_id FROM performances WHERE rowid = last_insert_rowid();")
            s = c.fetchone()
        else:
            s = "No such movie or theater"

    else:
        query = """
            SELECT p_id,date,time,title,prod_year,t_name,capacity-coalesce(count(id),0)
            FROM performances
            JOIN movies
            USING(imdb_id)
            JOIN theaters
            USING(t_name)
            LEFT JOIN tickets
            USING(p_id)
            """
        c = conn.cursor()
        c.execute(query)
        a = [{"performanceId":p_id,"date":date,"startTime":time,"title":title,"year":prod_year,"theater":t_id,'remainingSeats':capacity}
            for (p_id,t_id,date,time,title,prod_year,capacity) in c]
        s={'data':a}

    return format_response(s)

@route('/tickets',methods=['GET','POST'])
def add_ticket():
    response.content_type = 'application/json'
    user = request.query.user
    p_id = request.query.performance
    pwd = request.query.pwd
    if (user and p_id and pwd):
        c = conn.cursor()
        query = """
            SELECT password
            FROM users
            WHERE username = ?
        """
        c.execute(query,[user])
        database_pw = c.fetchone()

        if(pwd == database_pw[0]):
            q = """
                SELECT capacity-coalesce(count(id),0)
                FROM performances
                LEFT JOIN tickets
                USING(p_id)
            """
            r_seats = c.fetchone()
            if(r_seats == 0):
                s= 'No remaining tickets'
            else:
                cticket = """
                    INSERT
                    INTO tickets(username,p_id)
                    VALUES (?,?)
                """
                c.execute(cticket,[user,p_id])
                conn.commit()
                t_id=c.execute("SELECT id FROM tickets WHERE rowid = last_insert_rowid();")
                s= c.fetchone()


        else:
            s = f'Wrong password' #given:{pwd} found:{database_pw[0]}
            response.status = 401
    else:
        s = 'Error'
        response.status = 400
    return format_response(s)
#http://localhost:7007/performances?imdb=tt5580390&theater=Kino&date=2019-02-22&time=19:00
'''