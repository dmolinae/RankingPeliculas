# -*- coding: utf-8 -*-
import sys
import sqlite3
from PySide import QtGui, QtCore
import os

def conectar():
	con = sqlite3.connect(str(os.getcwd())+"/db_movies/movies.db")
	con.row_factory = sqlite3.Row
	c = [con.cursor(),con]
	return c

def getDatos():
	'''Método para obtener las peliculas listados en la tabla "movies"'''
	c = conectar()[0]
	query = "SELECT * FROM movies ORDER BY ranking ASC"
	resultado = c.execute(query)
	datos = resultado.fetchall()
	return datos

def getDatoId(pk_id):
	'''Método para obtener la pelicula de la tabla movies que coincida con el id pk_id'''
	c = conectar()[0]
	query = "SELECT * FROM movies WHERE id = ?"
	resultado = c.execute(query, [pk_id])
	movie = resultado.fetchall()
	return movie

def getDatoRank(rank):
	c = conectar()[0]
	query = "SELECT * FROM movies WHERE ranking = ?"
	resultado = c.execute(query, [rank])
	movie = resultado.fetchall()
	return movie

def updateDatoRank(nombre,nuevo_rank):
	conex = conectar()
	c = conex[0]
	conn = conex[1]
	query = "UPDATE movies SET ranking = ? WHERE title = ?"
	c.execute(query, [nuevo_rank,nombre])
	conn.commit()

