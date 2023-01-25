from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
import math
import cross_section_img

views_belka_zelbetowa = Blueprint('views_belka_zelbetowa', __name__)



@views_belka_zelbetowa.route('/belka_zelbetowa', methods=['GET', 'POST'])
@login_required

def belka_zelbetowa():

	static_scheme = ""

	if request.method == 'POST':

		static_scheme = request.form.get('static_scheme')
		length = request.form.get('length')
		q_def = request.form.get('q_def')
		height = request.form.get('height')
		width = request.form.get('width')


		if 0 in [len(static_scheme), len(length), len(q_def), len(height), len(width)]:
			flash('Uzupełnij dane.')

		else:
			length = float(length)
			q_def = float(q_def)
			height = float(height)
			width = float(width)


			return redirect(url_for('views_belka_zelbetowa.belka_zelbetowa_02', static_scheme=static_scheme, length=length, q_def=q_def, height=height,
									width=width))


			# strength_class = request.form.get('strength_class')
			# diameter = request.form.get('diameter')
			# quantity = request.form.get('quantity')
			# cover = request.form.get('cover')
			# diameter_s = request.form.get('diameter_s')


			# cross_section_img()

		
	return render_template("belka_zelbetowa.html", user=current_user, static_scheme=static_scheme)




strength_classes = ["C12/15", "C16/20", "C20/25", "C25/30", "C30/37", "C35/45", "C40/50", "C45/55", "C50/60",
				"C55/67", "C60/75", "C70/85", "C80/95", "C90/105"]

f_ck_dict = {"C12/15":12, "C16/20":16, "C20/25":20, "C25/30":25, "C30/37":30, "C35/45":35, "C40/50":40,
			 "C45/55":45, "C50/60":50, "C55/67":55, "C60/75":60, "C70/85": 70, "C80/95": 80, "C90/105": 90}
			 
diameters = [6, 8, 10, 12, 16, 20, 25, 32, 40]


@views_belka_zelbetowa.route('/belka_zelbetowa_02', methods=['GET', 'POST'])
@login_required

def belka_zelbetowa_02():

	M_span = 0
	M_support = 0

	static_scheme = request.args.get('static_scheme')
	length = float(request.args.get('length'))
	q_def = float(request.args.get('q_def'))
	height = float(request.args.get('height'))
	width = float(request.args.get('width'))


	q_weight = 0.01*height*0.01*width*25

		
	if static_scheme == "swobodnie podparta":
		M_span = round((q_def+q_weight)*length**2/8, 3)

	elif static_scheme == "obustronnie utwierdzona":
		M_support = round(-(q_def+q_weight)*length**2/12, 3)
		M_span = round((q_def+q_weight)*length**2/24, 3)



	return render_template("belka_zelbetowa_02.html", user=current_user, static_scheme=static_scheme, M_span=M_span, M_support=M_support, length=length,
							height=height, q_def=q_def, width=width, strength_classes=strength_classes, f_ck_dict=f_ck_dict, diameters=diameters)





#pamiętać o przekazaniu zmiennych jako argumentów funkcji render_template, jeśli html ma jakiejś z nich użyć z backendu!