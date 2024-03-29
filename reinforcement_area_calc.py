import math


def reinf_area_calc(M_span, width, height, des_sit, strength_class, f_ck, cover, diameter_s, bottom_def_dia, top_def_dia):

	M_ed = M_span
	b = 0.01*width
	h = 0.01*height

	if des_sit == "persistent or transient":
		gamma_c = 1.5
		gamma_s = 1.15

	if des_sit == "accidental":
		gamma_c = 1.2
		gamma_s = 1.0

	#concrete parameters
	alpha = 1
	f_cd = alpha*f_ck/gamma_c
	#steel parameters
	f_yk = 500
	f_yd = f_yk/gamma_s
	E_s = 200000

	if f_ck <= 50:
		lambd = 0.8
		eta = 1
	if f_ck > 50:
		lambd = 0.8 - (f_ck-50)/400
		eta = 1 - (f_ck-50)/200

	epsilon_cu3_dict = {"C12/15":0.0035, "C16/20":0.0035, "C20/25":0.0035, "C25/30":0.0035, "C30/37":0.0035, "C35/45":0.0035, "C40/50":0.0035,
						 "C45/55":0.0035, "C50/60":0.0035, "C55/67":0.0031, "C60/75":0.0029, "C70/85": 0.0027, "C80/95": 0.0026, "C90/105": 0.0026}

	epsilon_cu3 = epsilon_cu3_dict[strength_class]

	a_1 = 0.001*(cover + diameter_s + bottom_def_dia/2)
	a_2 = 0.001*(cover + diameter_s + top_def_dia/2)

	d = h - a_1

	xi_lim = lambd * epsilon_cu3/(epsilon_cu3 + f_yd/E_s)
	zeta_lim = 1 - 0.5*xi_lim
	A_0_lim = xi_lim*zeta_lim
	A_0 = M_ed/(eta*f_cd*1000*b*d**2)

	if A_0 <= A_0_lim:

		#reinforcement for compression is not required
		zeta = (1+((1-2*A_0)**(0.5)))/2
		A_s1_req = M_ed/(f_yd*1000*zeta*d)
		A_s2_req = 0

	else:
		#reinforcement for compression is required
		M_Rd_lim = A_0_lim*eta*f_cd*1000*b*d**2
		A_s1_1 = xi_lim*b*d*eta*f_cd/f_yd
		A_s1_2 = (M_ed - M_Rd_lim)/f_yd*1000*(d - a_2)
		A_s1_req = A_s1_1 + A_s1_2
		A_s2_req = A_s1_2

	A_s1_req = 10000*A_s1_req
	A_s2_req = 10000*A_s2_req

	f_cm = f_ck + 8

	if f_ck < 55:
		f_ctm = 0.30*f_ck**(2/3)
	else:
		f_ctm = 2.12*math.log(1+0.1*f_cm)

	A_smin = max(0.26*f_ctm/f_yk*b*d, 0.0013*b*d)
	A_smin = 10000*A_smin

	A_smax = 0.04*b*h
	A_smax = 10000*A_smax

	return A_s1_req, A_s2_req, A_0, A_0_lim, A_smin, A_smax


def bending_moment_resistance(M_span, width, height, des_sit, strength_class, f_ck, cover, diameter_s, diameter11, quantity11, diameter12, quantity12,
								diameter11top, quantity11top, A_s1, A_s2):


	M_ed = M_span
	b = 0.01*width
	h = 0.01*height

	if des_sit == "persistent or transient":
		gamma_c = 1.5
		gamma_s = 1.15

	if des_sit == "accidental":
		gamma_c = 1.2
		gamma_s = 1.0

	#concrete parameters
	alpha = 1
	f_cd = alpha*f_ck/gamma_c
	#steel parameters
	f_yk = 500
	f_yd = f_yk/gamma_s
	E_s = 200000

	if f_ck <= 50:
		lambd = 0.8
		eta = 1
	if f_ck > 50:
		lambd = 0.8 - (f_ck-50)/400
		eta = 1 - (f_ck-50)/200

	epsilon_cu3_dict = {"C12/15":0.0035, "C16/20":0.0035, "C20/25":0.0035, "C25/30":0.0035, "C30/37":0.0035, "C35/45":0.0035, "C40/50":0.0035,
						 "C45/55":0.0035, "C50/60":0.0035, "C55/67":0.0031, "C60/75":0.0029, "C70/85": 0.0027, "C80/95": 0.0026, "C90/105": 0.0026}

	epsilon_cu3 = epsilon_cu3_dict[strength_class]

	a_1 = 0.001*(cover + diameter_s + (quantity11*diameter11+quantity12*diameter12)/(quantity11+quantity12)/2)

	a_2 = 0.001*(cover + diameter_s + diameter11top/2)

	#converting A_s1, A_s2 from [cm2] to [m2]
	A_s1 = 0.01*0.01*A_s1
	A_s2 = 0.01*0.01*A_s2

	d = h - a_1

	x_lim = epsilon_cu3*d/(epsilon_cu3 + f_yd/E_s)
	x_yd_min = epsilon_cu3*a_2/(epsilon_cu3 - f_yd/E_s)
	x_neg_yd_min = epsilon_cu3*a_2/(epsilon_cu3 + f_yd/E_s)
	
	x = 1/lambd*f_yd*(A_s1-A_s2)/(eta*f_cd*b)

	if x < x_yd_min:

		sigma_s1 = f_yd

		A = (epsilon_cu3*E_s*A_s2 - f_yd*A_s1)/(eta*f_cd*b)
		B = 4*lambd*epsilon_cu3*E_s*A_s2/(eta*f_cd*b)*a_2

		x = 1/lambd*(-A+(A**2+B)**(1/2))/2

		if x < x_neg_yd_min:

			x = 1/lambd*f_yd*(A_s1+A_s2)/(eta*f_cd*b)
			sigma_s2 = -f_yd

		else:
			sigma_s2 = epsilon_cu3*E_s*(x-a_2)/x

	else:
		sigma_s2 = f_yd

		if x <= x_lim:
			sigma_s1 = f_yd

		else:
			x = x_lim
			sigma_s1 = (eta*f_cd*b*lambd*x + f_yd*A_s2)/A_s1

	M_Rd = eta*f_cd*1000*b*lambd*x*(d-0.5*lambd*x) + sigma_s2*1000*A_s2*(d-a_2)
	M_Rd = round(M_Rd, 3)

	return M_Rd





