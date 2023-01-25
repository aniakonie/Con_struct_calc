from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json
import math

views_zakotwienie = Blueprint('views_zakotwienie', __name__)


strength_classes = ["C12/15", "C16/20", "C20/25", "C25/30", "C30/37", "C35/45", "C40/50", "C45/55", "C50/60",
				"C55/67", "C60/75", "C70/85", "C80/95", "C90/105"]

f_ck_dict = {"C12/15":12, "C16/20":16, "C20/25":20, "C25/30":25, "C30/37":30, "C35/45":35, "C40/50":40,
			 "C45/55":45, "C50/60":50, "C55/67":55, "C60/75":60, "C70/85": 70, "C80/95": 80, "C90/105": 90}
			 
diameters = [6, 8, 10, 12, 16, 20, 25, 32, 40]


@views_zakotwienie.route('/zakotwienie', methods=['GET', 'POST'])
@login_required

def zakotwienie():


	strength_class = " "
	f_ck = " "
	l_brqd = " "


	if request.method == 'POST':
		strength_class = request.form.get('strength_class')
		f_ck = f_ck_dict[strength_class]
		f_cm = f_ck + 8

		if f_ck < 55:
			f_ctm = 0.30*f_ck**(2/3)
		else:
			f_ctm = 2.12*math.log(1+0.1*f_cm)

		f_ctk_05 = 0.7*f_ctm


		if request.form.get('conditions') == "dobre":
			n1 = 1
		elif request.form.get('conditions') == "słabe":
			n1 = 0.7

		diameter = int(request.form.get('diameter'))

		if diameter < 40:
			n2 = 1
		else:
			n2=(132 - diameter)/100
		

		if request.form.get('des_sit') == "trwała i przejściowa":
			gamma_c = 1.5
		if request.form.get('des_sit') == "wyjątkowa":
			gamma_c = 1.2

		alpha_ct = 1

		f_ctd = alpha_ct*f_ctk_05/gamma_c

		f_bd = 2.25*n1*n2*f_ctd

		sigma_sd = 420 #naprężenie obliczeniowe w miejscu, od którego oblicza się długość zakotwienia (granica plast. stali)

		l_brqd = (1/4)*diameter*sigma_sd/f_bd
		l_brqd = round(l_brqd/10)
		print(l_brqd)

		
	return render_template("zakotwienie.html", user=current_user, strength_classes=strength_classes, strength_class=strength_class,
							f_ck=f_ck, diameters=diameters, l_brqd=l_brqd)



#pamiętać o przekazaniu zmiennych jako argumentów funkcji render_template, jeśli html ma jakiejś z nich użyć z backendu!