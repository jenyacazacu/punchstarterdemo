import datetime

from flask import Flask, render_template, request, redirect, url_for, abort
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.migrate import Migrate, MigrateCommand

import cloudinary.uploader





app = Flask(__name__)
app.config.from_object('punchstarter.default_settings')
manager = Manager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from punchstarter.models import *	

@app.route('/')
def hello():
	projects = db.session.query(Project).order_by(Project.created_time.desc()).limit(15)
	
	return render_template("index.html", projects=projects)

@app.route('/projects/create', methods=['GET','POST'])
def create():
	if request.method == 'GET':
		return render_template("create.html")
	if request.method == 'POST':
		#handle the form submission
		now = datetime.datetime.now()
		time_end = request.form.get("funding_end_date")
		time_end = datetime.datetime.strptime(time_end,'%Y-%m-%d')

		cover_photo = request.files['cover_image']
		uploaded_image = cloudinary.uploader.upload(
			cover_photo,
			crop   = 'limit',
			width  = 680,
			height = 550
			)
		image_filename = uploaded_image["public_id"]

		new_project = Project(
				member_id = 1, # guest creatot 
				name = request.form.get('project_name'),
				short_description = request.form.get('short_description'),
				long_description = request.form.get('long_description'),
				image_filename = image_filename,
				goal_amount = request.form.get('funding_goal'),
				start_time = now,
				end_time = time_end,
				created_time = now
			)
		db.session.add(new_project)
		db.session.commit()

		return redirect(url_for('project_detail', project_id =new_project.id))

@app.route('/projects/<int:project_id>')
def project_detail(project_id):
	project = db.session.query(Project).get(project_id)
	if project is None:
		abort(404)

	return render_template("project_detail.html", project=project)

@app.route('/projects/<int:project_id>/pledge', methods=['GET','POST'])
def pledge(project_id):
	project = db.session.query(Project).get(project_id)
	if request.method == 'GET':
		if project is None:
			abort(404)
		return render_template("pledge.html", project = project)
	if request.method == 'POST':
		#handle the form submission
		now = datetime.datetime.now()
		new_pledge = Pledge(
			member_id = 1,
			project_id = project_id,
			amount = request.form.get('amount'),
			time_created = now
			)

		db.session.add(new_pledge)
		db.session.commit()
		return redirect(url_for('project_detail', project_id=project.id))

@app.route('/search/')
def search():
	query = request.args.get("q") or ""
	projects = db.session.query(Project).filter(
		Project.name.ilike('%'+ query +'%') |
		Project.short_description.ilike('%'+ query + '%') |
		Project.long_description.ilike('%'+ query + '%')
		).all()

	project_count = len(projects)

	return render_template('search.html',
		query_text = query,
		projects = projects,
		project_count = project_count
		)








