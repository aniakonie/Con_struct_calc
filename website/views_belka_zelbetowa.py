from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file, send_from_directory
from flask_login import login_required, current_user
from . import db
import json
import math
from cross_section_img import cross_section_img
from reinforcement_area_calc import reinf_area_calc, bending_moment_resistance

views_belka_zelbetowa = Blueprint('views_belka_zelbetowa', __name__)


strength_classes = ["C12/15", "C16/20", "C20/25", "C25/30", "C30/37", "C35/45", "C40/50", "C45/55", "C50/60",
					"C55/67", "C60/75", "C70/85", "C80/95", "C90/105"]

f_ck_dict = {"C12/15":12, "C16/20":16, "C20/25":20, "C25/30":25, "C30/37":30, "C35/45":35, "C40/50":40,
			 "C45/55":45, "C50/60":50, "C55/67":55, "C60/75":60, "C70/85": 70, "C80/95": 80, "C90/105": 90}
			 
diameters = [6, 8, 10, 12, 16, 20, 25, 32, 40]



@views_belka_zelbetowa.route('/belka_zelbetowa', methods=['GET', 'POST'])
@login_required

def belka_zelbetowa():

	if request.method == 'POST':

		static_scheme = request.form.get('static_scheme')
		length = request.form.get('length')
		height = request.form.get('height')
		width = request.form.get('width')
		q_def = request.form.get('q_def')
		des_sit = request.form.get('des_sit')
		strength_class = request.form.get('strength_class')
		diameter_s = request.form.get('diameter_s')
		bottom_def_dia = request.form.get('bottom_def_dia')
		top_def_dia = request.form.get('top_def_dia')
		cover = request.form.get('cover')

		if '' in {length, height, width, q_def, cover}:
			flash('Uzupełnij dane.')

		else:

			return redirect(url_for('views_belka_zelbetowa.belka_zelbetowa_02', static_scheme=static_scheme, length=length, height=height,
								width=width, q_def=q_def, des_sit=des_sit, strength_class=strength_class, diameter_s=diameter_s,
								bottom_def_dia=bottom_def_dia, top_def_dia=top_def_dia, cover=cover))

		
	return render_template("belka_zelbetowa.html", user=current_user, strength_classes=strength_classes, diameters=diameters)



@views_belka_zelbetowa.route('/belka_zelbetowa_02', methods=['GET', 'POST'])
@login_required

def belka_zelbetowa_02():


	M_Rd = A_s1 = A_s2 = A_s1_req = A_s2_req = A_0 = A_0_lim = A_smin = A_smax = M_span = M_support = static_scheme = ""

	static_scheme = request.args.get('static_scheme')
	length = float(request.args.get('length'))
	height = int(request.args.get('height'))
	width = int(request.args.get('width'))
	q_def = float(request.args.get('q_def'))
	des_sit = request.args.get('des_sit')
	strength_class = request.args.get('strength_class')
	diameter_s = int(request.args.get('diameter_s'))
	bottom_def_dia = int(request.args.get('bottom_def_dia'))
	top_def_dia = int(request.args.get('top_def_dia'))
	cover = int(request.args.get('cover'))


	f_ck = f_ck_dict[strength_class]

	q_weight = 0.01*height*0.01*width*25


	if static_scheme == "swobodnie podparta":
		M_span = round((q_def+q_weight)*length**2/8, 3)

	elif static_scheme == "obustronnie utwierdzona":
		M_support = round(-(q_def+q_weight)*length**2/12, 3)
		M_span = round((q_def+q_weight)*length**2/24, 3)


	A_s1_req, A_s2_req, A_0, A_0_lim, A_smin, A_smax = reinf_area_calc(M_span, width, height, des_sit, strength_class, f_ck, cover, diameter_s, bottom_def_dia, top_def_dia)


	#include algorithm which suggests rebar 


	A_s1_req = round(A_s1_req, 2)
	A_s2_req = round(A_s2_req, 2)
	A_smin = round(A_smin, 2)


	if request.method == 'POST':

		diameter11 = int(request.form.get('diameter11'))
		quantity11 = int(request.form.get('quantity11'))
		diameter12 = int(request.form.get('diameter12'))
		quantity12 = int(request.form.get('quantity12'))
		diameter11top = int(request.form.get('diameter11top'))
		quantity11top = int(request.form.get('quantity11top'))
		

		if (quantity11%2 == 1 and quantity12%2 == 1):
			flash('Liczby sztuk obu typów prętów nie mogą być obie nieparzyste (brak symetrii zbrojenia w przekroju).')


		width_rebar_mm = width*10 - 2*cover - 2*diameter_s
		rebar_spacing = (width_rebar_mm - quantity11*diameter11 - quantity12*diameter12)/(quantity11 + quantity12 - 1)

		d_g = 16
		k_1 = 1
		k_2 = 5


		if rebar_spacing < min(diameter11, diameter12):
			flash('Rozstaw prętów musi być większy niż największa z przyjętych średnic pręta.')

		elif rebar_spacing < (d_g + k_2):
			flash('Rozstaw prętów musi być większy niż średnica kruszywa powiększona o 5mm (przyjęta średnica kruszywa: 16mm).')

		elif rebar_spacing < 20:
			flash('Rozstaw prętów musi być większy niż 20mm.')

		else:
			cross_section_img(diameter11, diameter12, diameter11top, quantity11, quantity12, quantity11top, cover, diameter_s, height, width)

			A_s1 = 0.01*3.14159*(quantity11*diameter11**2/4 + quantity12*diameter12**2/4)
			A_s2 = 0.01*3.14159*quantity11top*diameter11top**2/4

			M_Rd = bending_moment_resistance(M_span, width, height, des_sit, strength_class, f_ck, cover, diameter_s, diameter11, quantity11, diameter12, quantity12,
											diameter11top, quantity11top, A_s1, A_s2)


			as1 = round(0.01*3.14159*(quantity11*diameter11**2/4 + quantity12*diameter12**2/4), 2)

			f = open("Wyniki_belka_zelbetowa.txt", "w", encoding="utf-8")
			f.write(f"Przyjęta powierzchnia zbrojenia dolnego wynosi: {as1}cm2")
			f.close()



	return render_template("belka_zelbetowa_02.html", user=current_user, static_scheme=static_scheme, M_span=M_span, M_support=M_support, length=length,
							height=height, q_def=q_def, width=width, f_ck_dict=f_ck_dict, diameters=diameters, des_sit=des_sit, A_s1_req=A_s1_req, A_s2_req=A_s2_req,
							A_0=A_0, A_0_lim=A_0_lim, A_smin=A_smin, A_smax=A_smax, A_s1=A_s1, A_s2=A_s2, M_Rd=M_Rd)




@views_belka_zelbetowa.route('/belka_zelbetowa_wyniki/')
@login_required

def belka_zelbetowa_wyniki():
	return send_file('C:\\Users\\konie\\OneDrive\\STUFF\\CODING\\01 ZAKOTWIENIE PRĘTÓW\\website\\static\\Wyniki_belka_zelbetowa.txt', as_attachment=True)