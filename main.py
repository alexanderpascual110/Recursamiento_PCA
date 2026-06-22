from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)

cadena = "mongodb+srv://alexanderpasc24_db_user:alex060609@alex01.p8q4arl.mongodb.net/?appName=Alex01"
cliente = MongoClient(cadena)
db = cliente["escuela"]

maestros = db["maestros"]
alumnos = db["alumnos"]
materias = db["materias"]
grupos = db["grupos"]

@app.route("/")
def inicio():
    return render_template("index.html")



@app.route("/maestros")
def ver_maestros():
    datos = maestros.find()
    return render_template("maestros.html", datos=datos)

@app.route("/agregar_maestro", methods=["POST"])
def agregar_maestro():

    maestros.insert_one({
        "nombre": request.form["nombre"],
        "especialidad": request.form["especialidad"],
        "telefono": request.form["telefono"],
        "turno": request.form["turno"],
        "numero_de_empleado": request.form["numero_de_empleado"]
    })

    return redirect("/maestros")

@app.route("/eliminar_maestro/<id>")
def eliminar_maestro(id):
    maestros.delete_one({"_id": ObjectId(id)})
    return redirect("/maestros")

@app.route("/editar_maestro/<id>")
def editar_maestro(id):

    dato = maestros.find_one({"_id": ObjectId(id)})
    return render_template(
        "editar_maestro.html",
        dato=dato
    )

@app.route("/actualizar_maestro/<id>", methods=["POST"])
def actualizar_maestro(id):

    maestros.update_one(
        {"_id": ObjectId(id)},
        {"$set":{
            "nombre": request.form["nombre"],
            "especialidad": request.form["especialidad"],
            "telefono": request.form["telefono"],
            "turno": request.form["turno"],
            "numero_de_empleado": request.form["numero_de_empleado"]
        }}
    )

    return redirect("/maestros")



@app.route("/alumnos")
def ver_alumnos():
    datos = alumnos.find()
    return render_template("alumnos.html", datos=datos)

@app.route("/agregar_alumno", methods=["POST"])
def agregar_alumno():

    fecha_nacimiento = request.form["fecha_de_nacimiento"]

    fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")

    if fecha < datetime(2008,1,1) or fecha > datetime(2011,12,31):
        return "La fecha debe estar entre 2008 y 2011"

    alumnos.insert_one({
        "nombre": request.form["nombre"],
        "grupo": request.form["grupo"],
        "correo": request.form["correo"],
        "fecha_de_nacimiento": request.form["fecha_de_nacimiento"]
        
    })

    return redirect("/alumnos")

@app.route("/eliminar_alumno/<id>")
def eliminar_alumno(id):
    alumnos.delete_one({"_id": ObjectId(id)})
    return redirect("/alumnos")

@app.route("/editar_alumno/<id>")
def editar_alumno(id):

    dato = alumnos.find_one({"_id": ObjectId(id)})
    return render_template(
        "editar_alumno.html",
        dato=dato
    )

@app.route("/actualizar_alumno/<id>", methods=["POST"])
def actualizar_alumno(id):

    alumnos.update_one(
        {"_id": ObjectId(id)},
        {"$set":{
            "nombre": request.form["nombre"],
            "grupo": request.form["grupo"],
            "correo": request.form["correo"],
            "fecha_de_nacimiento": request.form["fecha_de_nacimiento"]
        }}
    )

    return redirect("/alumnos")


@app.route("/materias")
def ver_materias():
    datos = materias.find()
    return render_template("materias.html", datos=datos)

@app.route("/agregar_materia", methods=["POST"])
def agregar_materia():

    materias.insert_one({
        "nombre": request.form["nombre"],
        "codigo_de_la_materia": request.form["codigo_de_la_materia"],
        "horas_semanales": request.form["horas_semanales"],
        "creditos": request.form["creditos"]
    })

    return redirect("/materias")

@app.route("/eliminar_materia/<id>")
def eliminar_materia(id):
    materias.delete_one({"_id": ObjectId(id)})
    return redirect("/materias")

@app.route("/editar_materia/<id>")
def editar_materia(id):

    dato = materias.find_one({"_id": ObjectId(id)})
    return render_template(
        "editar_materia.html",
        dato=dato
    )

@app.route("/actualizar_materia/<id>", methods=["POST"])
def actualizar_materia(id):

    materias.update_one(
        {"_id": ObjectId(id)},
        {"$set":{
            "nombre": request.form["nombre"],
            "codigo_de_la_materia": request.form["codigo_de_la_materia"],
            "horas_semanales": request.form["horas_semanales"],
            "creditos": request.form["creditos"]
        }}
    )

    return redirect("/materias")

@app.route("/grupos")
def ver_grupos():

    lista_maestros = maestros.find()
    lista_materias = materias.find()
    lista_alumnos = alumnos.find()
    lista_grupos = grupos.find()

    return render_template(
        "mantenimiento_grupos.html",
        maestros=lista_maestros,
        materias=lista_materias,
        alumnos=lista_alumnos,
        grupos=lista_grupos
    )

@app.route("/guardar_grupo", methods=["POST"])
def guardar_grupo():

    grupos.insert_one({

        "grupo": request.form["grupo"],
        "especialidad": request.form["especialidad"],
        "maestro": request.form["maestro"],
        "materia": request.form["materia"]

    })

    return redirect("/grupos")

app.run(debug=True)